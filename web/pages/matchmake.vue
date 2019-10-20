<template>
  <v-form>
    <v-container>
      <v-layout row wrap>
        <v-container grid-list-md fluid>
          <v-list>
            <v-layout col wrap>
              <v-flex
                v-for="player in players"
                :key="player.id"
                xs12
                md3
                @click.stop="togglePlayerSelected(player.id)"
              >
                <v-list-tile @click="() => {}">
                  <v-list-tile-action>
                    <v-checkbox :value="playerSelected[player.id]"></v-checkbox>
                  </v-list-tile-action>

                  <v-list-tile-content>
                    <v-list-tile-title>{{ player.user.username }}</v-list-tile-title>
                  </v-list-tile-content>
                </v-list-tile>
              </v-flex>
            </v-layout>
          </v-list>
        </v-container>

        <v-flex xs12>
          <v-flex
            v-for="(matchup, index) in matchups"
            :key="index"
            xs12
          >
            <v-layout justify-center>
              <v-flex xs12 sm6 md4 lg3>
                <match-result-card
                  :left-players="matchup.teams[0]"
                  :right-players="matchup.teams[1]"
                  :left-score="1"
                  :right-score="0"
                >
                  <template v-slot:center>
                    {{ (100 * matchup.quality).toFixed(2) }}%
                  </template>
                </match-result-card>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-flex>

        <v-flex xs12>
          <v-layout row justify-end>
            <v-btn to="/">Zurück</v-btn>
            <v-btn
              color="primary"
              @click="submit"
            >
              Berechnen
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import MatchResultCard from '../components/match-result-card.vue'

export default {
  components: {
    MatchResultCard,
  },
  data() {
    return {
      playerSelected: {},
      matchups: [],
    }
  },
  methods: {
    togglePlayerSelected(playerId) {
      const selected = this.playerSelected[playerId] === true
      this.$set(this.playerSelected, playerId, !selected)
    },
    async submit() {
      const query = [...Object.keys(this.playerSelected)]
        .map((id) => 'id=' + id)
        .join('&')
      const response = await this.$axios.$get('/players/matchmake/?' + query)
      const matchups = response.results
      this.matchups = matchups.map(matchup => ({
        ...matchup,
        teams: matchup.teams.map(team =>
          team.map(playerId =>
            this.players.find(player => player.id === playerId)))
      }))
    },
  },
  computed: {
    ...mapState({
      players: (state) => state.players,
    })
  },
}
</script>
