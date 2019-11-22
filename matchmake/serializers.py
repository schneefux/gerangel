import itertools
import math
from rest_framework import serializers
from trueskill import TrueSkill

from matchlog.serializers import PlayerSerializer


def win_probability(env, team1, team2):
    '''
    @return win probability for team 1
    '''
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (env.beta * env.beta) + sum_sigma)
    return env.cdf(delta_mu / denom)


class MatchupSerializer(serializers.ListSerializer):
  child = PlayerSerializer()

  def to_representation(self, data):
    players = data
    env = TrueSkill()
    possible_teams = itertools.combinations_with_replacement(players, 2)
    possible_teams = [set(t) for t in possible_teams]
    possible_matchups = itertools.combinations(possible_teams, 2)
    all_players_distinct = lambda h, a: len(set(h) - set(a)) == len(set(h))
    possible_matchups = [(h, a) for h, a in possible_matchups if all_players_distinct(h, a)]
    matchup_qualities = []

    for home_players, away_players in possible_matchups:
      home_ratings = [env.create_rating(
        mu=p.rating_mu, sigma=p.rating_sigma)
        for p in home_players
      ]
      away_ratings = [env.create_rating(
        mu=p.rating_mu, sigma=p.rating_sigma)
        for p in away_players
      ]
      rating_groups = [home_ratings, away_ratings]

      quality = env.quality(rating_groups)
      win_probability_home = win_probability(env, home_ratings, away_ratings)

      home_ids = [p.id for p in home_players]
      away_ids = [p.id for p in away_players]
      matchup_qualities.append({
        "teams": [home_ids, away_ids],
        "win_probability": [win_probability_home, 1 - win_probability_home],
        "quality": quality
      })

    matchup_qualities = sorted(matchup_qualities,
      key=lambda m: m["quality"], reverse=True)
    return matchup_qualities