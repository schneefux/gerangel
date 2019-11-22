<template>
  <v-form>
    <v-container>
      <h1>Matchmaking</h1>
      <v-layout row wrap>
        <v-flex xs12>
          <v-text-field
            v-model="playerSearch"
            append-icon="search"
            label="Spieler suchen"
            single-line
            hide-details
          />
        </v-flex>
        <v-flex xs12>
          <v-data-table
            v-model="selectedPlayers"
            :headers="[
              { text: 'Verfügbar', value: 'selected', sortable: false },
              { text: 'Benutzername', value: 'name', sortable: false },
              { text: 'TrueSkill-Wertung', value: 'rating' }
            ]"
            :items="tablePlayers"
            :search="playerSearch"
            :rows-per-page-items="[10, 50, 100]"
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
                <match-result-card :teams="matchup.teams">
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
import { mapState, mapGetters, mapActions } from 'vuex'
import MatchResultCard from '../components/match-result-card.vue'

export default {
  components: {
    MatchResultCard,
  },
  data() {
    return {
      playerSearch: '',
      selectedPlayers: [],
      matchups: [],
    }
  },
  methods: {
    async submit() {
      const query = this.selectedPlayers
        .map((player) => 'id=' + player.id)
        .join('&')
      const response = await this.$axios.$get('/matchmake/?' + query)
      const matchups = response.results
      this.matchups = matchups.map(matchup => ({
        quality: matchup.quality,
        teams: matchup.teams.map((team, index) => ({
          score: matchup.win_probability[index],
          players: team,
        }))
      }))
    },
  },
  computed: {
    minPoolSizeReached() {
      return this.selectedPlayers.length >= 2
    },
    tablePlayers() {
      return this.players.map((player) => ({
        id: player.id,
        name: player.user.username,
        rating: player.rating,
      }))
    },
    ...mapGetters({
      getPlayerById: 'getPlayerById',
    }),
    ...mapState({
      players: (state) => state.players,
    })
  },
}
</script>
