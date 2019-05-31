from matchlog.models import Match
from trueskill import TrueSkill
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Match)
def rate_match(sender, instance, created, **kwargs):
  if not created:
    return

  env = TrueSkill()

  home_rating = env.create_rating(
    mu=instance.home_player.rating_mu,
    sigma=instance.home_player.rating_sigma)
  away_rating = env.create_rating(
    mu=instance.away_player.rating_mu,
    sigma=instance.away_player.rating_sigma)

  draw = instance.home_score == instance.away_score
  home_won = instance.home_score > instance.away_score

  rating_groups = [(home_rating, ), (away_rating, )]
  if draw:
    ranks = [0, 0]
  else:
    ranks = [1 if home_won else 0, 0 if home_won else 1]

  rating_groups = env.rate(rating_groups, ranks)

  home_rating = rating_groups[0][0]
  away_rating = rating_groups[1][0]

  instance.home_player.rating_mu = home_rating.mu
  instance.home_player.rating_sigma = home_rating.sigma
  instance.home_player.save()
  instance.away_player.rating_mu = away_rating.mu
  instance.away_player.rating_sigma = away_rating.sigma
  instance.away_player.save()
