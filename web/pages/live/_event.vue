<template>
  <v-stepper v-model="step">
    <v-stepper-header>
      <v-stepper-step step="1">Teams zuordnen</v-stepper-step>
      <v-stepper-step step="2">Positionen zuordnen</v-stepper-step>
      <v-stepper-step step="3">Sätze erfassen</v-stepper-step>
      <v-stepper-step step="4">Daten überprüfen</v-stepper-step>
    </v-stepper-header>

    <match-result-sets-card
      v-if="matchResult !== undefined && step !== 4"
      :teams="matchResult.teams"
      :sets="matchResult.sets"
      :date="new Date()"
    />

    <v-stepper-items>
      <v-stepper-content step="1">
        <v-container grid-list-md>
          <v-layout row wrap>
            <v-flex d-flex>
              <p>
                Spieler durch ziehen und loslassen zu Teams zuordnen.
              </p>
            </v-flex>
            <v-flex
              v-if="teamsFixed"
              d-flex
            >
              <v-btn @click="swapColors()">
                <v-icon left>mdi-swap-horizontal</v-icon>
                Teams Tauschen
              </v-btn>
            </v-flex>
            <v-flex
              v-if="!teamsFixed"
              xs12
            >
              <v-card
                min-height="10rem"
                v-show="playersWithoutColor.length > 0"
              >
                <v-card-title>
                  Ohne Team
                </v-card-title>
                <draggable
                  v-model="playersWithoutColor"
                  group="players"
                  class="h-full w-full"
                >
                  <v-btn
                    v-for="player in playersWithoutColor"
                    :key="player"
                  >
                    {{ getPlayerById(player).user.username }}
                  </v-btn>
                </draggable>
              </v-card>
            </v-flex>
            <v-flex
              v-for="color in colors"
              :key="color"
              xs6
            >
              <v-card min-height="10rem">
                <v-card-title>
                  Team {{ color }}
                </v-card-title>
                <v-layout row wrap class="h-full">
                  <draggable
                    v-model="playersByColor[color]"
                    :disabled="teamsFixed"
                    group="players"
                    class="w-full h-full"
                    @change="e => colorDragEvent(color, e)"
                  >
                    <v-btn
                      v-for="player in playersByColor[color]"
                      :key="player"
                      :disabled="teamsFixed"
                    >
                      {{ getPlayerById(player).user.username }}
                    </v-btn>
                  </draggable>
                </v-layout>
              </v-card>
            </v-flex>
            <v-flex d-flex>
              <v-btn
                v-if="!teamsFixed"
                :disabled="playersWithoutColor.length > 0"
                color="primary"
                @click="step++; teamsFixed = true"
              >
                Teams festlegen
              </v-btn>
              <v-btn
                v-else
                color="primary"
                @click="step++"
              >
                Farben festlegen
              </v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-container grid-list-md>
          <v-layout row wrap>
            <v-flex xs12>
              <p>
                Spieler durch ziehen und loslassen zu Positionen zuordnen.
              </p>
            </v-flex>
            <v-flex
              v-for="position in positions"
              :key="position"
              xs12
            >
              <v-card min-height="10rem">
                <v-card-title>
                  Position {{ position }}
                </v-card-title>
                <v-layout row wrap class="h-full">
                  <draggable
                    v-model="playersByPosition[position]"
                    group="players"
                    class="w-full h-full"
                    @change="e => positionDragEvent(position, e)"
                  >
                    <v-btn
                      v-for="player in playersByPosition[position]"
                      :key="player"
                    >
                      {{ getPlayerById(player).user.username }}
                    </v-btn>
                  </draggable>
                </v-layout>
              </v-card>
            </v-flex>
            <v-flex d-flex>
              <v-btn
                color="primary"
                @click="step++; dispatchLog('start_set', user.id)"
              >
                Satz beginnen
              </v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-container grid-list-md>
          <v-layout row wrap>
            <v-flex xs12>
              <p>
                Klicke Torschützen an.
              </p>
            </v-flex>
            <v-flex
              v-for="color in colors"
              :key="color"
              class="my-2"
              xs6
            >
              <v-layout column>
                <v-btn
                  v-for="player in playersByColor[color]"
                  :key="player"
                  large
                  @click="dispatchLog('score_goal', player)"
                >
                  {{ getPlayerById(player).user.username }}
                </v-btn>
              </v-layout>
            </v-flex>
            <v-flex d-flex>
              <v-btn
                color="secondary"
                @click="step = 1; dispatchLog('close_set', user.id)"
              >
                <v-icon left>mdi-repeat</v-icon>
                Satz beenden
              </v-btn>
            </v-flex>
            <v-flex d-flex>
              <v-btn
                color="primary"
                @click="step++; dispatchLog('close_set', user.id); loadMatchResult()"
              >
                <v-icon left>mdi-stop</v-icon>
                Spiel beenden
              </v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-stepper-content>

      <v-stepper-content step="4">
        <v-container grid-list-md>
          <v-layout row wrap>
            <v-flex d-flex>
              <p>
                Überprüfe das Ergebnis.
              </p>
            </v-flex>
            <v-flex
              v-if="matchResult !== undefined"
              xs12
            >
              <match-result-sets-card
                :teams="matchResult.teams"
                :sets="matchResult.sets"
                :date="new Date()"
              />
            </v-flex>
            <v-flex d-flex>
              <v-btn
                color="primary"
                @click="saveMatchResult()"
              >
                Eintragen
              </v-btn>
            </v-flex>
          </v-layout>
        </v-container>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'
import draggable from 'vuedraggable'
import MatchResultSetsCard from '~/components/match-result-sets-card'

export default {
  components: {
    draggable,
    MatchResultSetsCard,
  },
  data() {
    return {
      step: 1,
      colors: ['red', 'blue'],
      positions: ['flex', 'attack', 'defense'],
      playersByColor: { 'red': [], 'blue': [] },
      teamsFixed: false,
      matchResult: undefined,
      lastLogId: 0,
      refreshTimer: undefined,
    }
  },
  async asyncData({ query, params }) {
    const players = query.players.split(',').map(n => parseInt(n))
    return {
      playersWithoutColor: players,
      playersByPosition: {
        'flex': players,
        'attack': [],
        'defense': [],
      },
      eventId: params.event,
    }
  },
  async created() {
    await this.refreshLog()
  },
  methods: {
    async refreshLog() {
      if (this.refreshTimer !== undefined) {
        clearTimeout(this.refreshTimer)
      }

      const response = await this.$axios.$get('/log/?event.id=' + this.eventId + '&id_gt=' + this.lastLogId)
      if (this.teamsFixed) {
        await this.loadMatchResult()
      }

      const newLogs = response.results
      if (newLogs.length > 0) {
        this.lastLogId = newLogs[newLogs.length - 1].id
      }

      newLogs.forEach((log) => {
        const isNotPlayer = p => p !== log.player
        switch (log.action) {
          case 'change_color':
            if (!this.playersByColor[log.payload].includes(log.player)) {
              this.playersWithoutColor = this.playersWithoutColor.filter(isNotPlayer)
              this.colors.forEach(color => this.$set(this.playersByColor, color, this.playersByColor[color].filter(isNotPlayer)))
              this.$set(this.playersByColor, log.payload, this.playersByColor[log.payload].concat(log.player))
            }
            break
          case 'change_position':
            if (!this.playersByPosition[log.payload].includes(log.player)) {
              this.positions.forEach(position => this.$set(this.playersByPosition, position, this.playersByPosition[position].filter(isNotPlayer)))
              this.$set(this.playersByPosition, log.payload, this.playersByPosition[log.payload].concat(log.player))
            }
            break
          case 'close_set':
            this.teamsFixed = true
            if (this.step <= 3) {
              this.step = 1
            }
            break
          case 'start_set':
            this.teamsFixed = true
            this.step = 3
            break
        }
      })

      this.refreshTimer = setTimeout(() => this.refreshLog(), 1000)
    },
    async colorDragEvent(color, event) {
      if (event.added) {
        const player = event.added.element
        await this.dispatchLog('change_color', player, color)
      }
    },
    async positionDragEvent(position, event) {
      if (event.added) {
        const player = event.added.element
        await this.dispatchLog('change_position', player, position)
      }
    },
    async loadMatchResult() {
      this.matchResult = await this.$axios.$get('/events/' + this.eventId + '/match_result/')
    },
    async saveMatchResult() {
      await this.$axios.$post('/match-results/', this.matchResult)
      this.$router.replace('/')
      // TODO optimize this
      await this.loadMatchResults()
      await this.loadPlayers()
    },
    async swapColors() {
      const bluePlayers = this.playersByColor['blue']
      this.playersByColor['blue'] = this.playersByColor['red']
      this.playersByColor['red'] = bluePlayers

      await Promise.all(this.playersByColor['blue'].map(async (player) =>
        this.dispatchLog('change_color', player, 'blue')
      ))
      await Promise.all(this.playersByColor['red'].map(async (player) =>
        this.dispatchLog('change_color', player, 'red')
      ))
    },
    async dispatchLog(action, player, payload) {
      const log = {
        event: this.eventId,
        action,
        player,
        payload,
      }
      await this.$axios.$post('/log/', log)
      await this.refreshLog()
    },
    ...mapActions({
      loadPlayers: 'loadPlayers',
      loadMatchResults: 'loadMatchResults',
    }),
  },
  computed: {
    ...mapGetters({
      getPlayerById: 'getPlayerById',
    }),
    ...mapState({
      user: (state) => state.user,
    })
  },
}
</script>

<style scoped>
.h-full {
  height: 100%;
}

.w-full {
  width: 100%;
}
</style>
