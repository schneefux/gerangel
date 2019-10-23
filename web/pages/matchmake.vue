<template>
  <v-form>
    <v-container>
      <h1>Matchmaking</h1>
      <v-layout row wrap>
        <v-flex xs12>
          <!-- TODO add search -->
          <v-data-table
            v-model="selectedPlayers"
            :headers="[
              { text: 'Verfügbar', value: 'selected', sortable: false },
              { text: 'Benutzername', value: 'name', sortable: false },
              { text: 'TrueSkill-Wertung', value: 'rating' }
            ]"
            :items="tablePlayers"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:items="props">
              <td>
                <v-checkbox
                  v-model="props.selected"
                  primary
                  hide-details
                />
              </td>
              <td>{{ props.item.name }}</td>
              <td>{{ Math.floor(props.item.rating) }}</td>
            </template>
          </v-data-table>
        </v-flex>

        <v-flex xs12>
          <v-layout row justify-end>
            <v-btn to="/">Zurück</v-btn>
            <v-btn
              :disabled="!minPoolSizeReached"
              color="primary"
              @click="submit"
            >
              Berechnen
            </v-btn>
          </v-layout>
        </v-flex>

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
      selectedPlayers: [],
      matchups: [],
    }
  },
  methods: {
    async submit() {
      const query = this.selectedPlayers
        .map((player) => 'id=' + player.id)
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
    minPoolSizeReached() {
      return this.selectedPlayers.length >= 4
    },
    tablePlayers() {
      return this.players.map((player) => ({
        id: player.id,
        name: player.user.username,
        rating: player.rating,
      }))
    },
    ...mapState({
      players: (state) => state.players,
    })
  },
}
</script>
