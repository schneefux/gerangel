<template>
  <v-form
    v-model="valid"
    ref="form"
    lazy-validation
  >
    <v-container>
      <v-layout row wrap>
        <v-flex xs12 md6>
          <h6 class="subheading">Heim</h6>
          <v-layout row justify-space-between>
            <v-flex xs8>
              <v-autocomplete
                v-model="homePlayerIds"
                :items="players"
                :rules="[requiredArray, differentFromAwayPlayers]"
                :disabled="sets.length > 0"
                item-text="user.username"
                item-value="id"
                label="Spieler"
                box
                chips
                deletable-chips
                clearable
                multiple
              ></v-autocomplete>
            </v-flex>
            <v-flex xs3>
              <v-text-field
                v-model="homeScore"
                :rules="scoreRules"
                :disabled="sets.length > 0"
                label="Punkte"
                type="number"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-flex>

        <v-flex xs12 md6>
          <h6 class="subheading">Gast</h6>
          <v-layout row justify-space-between>
            <v-flex xs8>
              <v-autocomplete
                v-model="awayPlayerIds"
                :items="players"
                :rules="[requiredArray, differentFromHomePlayers]"
                :disabled="sets.length > 0"
                item-text="user.username"
                item-value="id"
                label="Spieler"
                box
                chips
                deletable-chips
                clearable
                multiple
              ></v-autocomplete>
            </v-flex>
            <v-flex xs3>
              <v-text-field
                v-model="awayScore"
                :rules="scoreRules"
                :disabled="sets.length > 0"
                label="Punkte"
                type="number"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-flex>

        <v-flex xs12>
          <h6 class="subheading">Sätze (optional)</h6>
          <v-card
            v-for="(set, index) in sets"
            :key="index"
            class="mt-4"
          >
            <v-container grid-list-lg fluid>
              <v-layout row wrap justify-space-between>
                <v-flex xs2 class="my-auto">
                  <span>Heim</span>
                </v-flex>
                <v-flex xs7>
                  <v-radio-group
                    v-model="set.homeColor"
                    :rules="[required]"
                    row
                  >
                    <v-radio
                      label="rot"
                      color="red"
                      value="red"
                    />
                    <v-radio
                      label="blau"
                      color="blue"
                      value="blue"
                    />
                  </v-radio-group>
                </v-flex>
                <v-flex xs3>
                  <v-text-field
                    v-model="set.homePoints"
                    label="Tore"
                    type="number"
                    required
                  ></v-text-field>
                </v-flex>
                <v-flex xs2 class="my-auto">
                  <span>Gast</span>
                </v-flex>
                <v-flex xs7>
                  <v-radio-group
                    v-model="set.awayColor"
                    :rules="[required]"
                    row
                  >
                    <v-radio
                      label="rot"
                      color="red"
                      value="red"
                    />
                    <v-radio
                      label="blau"
                      color="blue"
                      value="blue"
                    />
                  </v-radio-group>
                </v-flex>
                <v-flex xs3>
                  <v-text-field
                    v-model="set.awayPoints"
                    label="Tore"
                    type="number"
                    required
                  ></v-text-field>
                </v-flex>
                <v-flex
                  v-show="homePlayerIds.length > 1"
                  v-for="(player, index) in homePlayers"
                  :key="player.id"
                  xs6
                >
                  <span>
                    Position von {{ player.user.username }}
                  </span>
                  <v-radio-group
                    v-model="set.homePositions[index]"
                    :rules="[required]"
                  >
                    <v-radio
                      label="Flexibel"
                      value="flexible"
                    />
                    <v-radio
                      label="Angriff"
                      value="attack"
                    />
                    <v-radio
                      label="Verteidigung"
                      value="defense"
                    />
                  </v-radio-group>
                </v-flex>
                <v-flex
                  v-show="awayPlayerIds.length > 1"
                  v-for="(player, index) in awayPlayers"
                  :key="player.id"
                  xs6
                >
                  <span>
                    Position von {{ player.user.username }}
                  </span>
                  <v-radio-group
                    v-model="set.awayPositions[index]"
                    :rules="[required]"
                  >
                    <v-radio
                      label="Flexibel"
                      value="flexible"
                    />
                    <v-radio
                      label="Angriff"
                      value="attack"
                    />
                    <v-radio
                      label="Verteidigung"
                      value="defense"
                    />
                  </v-radio-group>
                </v-flex>
              </v-layout>
              <v-btn
                fab
                absolute
                top
                right
                round
                small
                @click="removeSet(index)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-container>
          </v-card>
          <div class="mt-3">
            <v-btn
              :disabled="homePlayerIds.length == 0 || awayPlayerIds.length == 0"
              @click="addSet()"
              round
            >
              <v-icon left>mdi-plus</v-icon>
              neuer satz
            </v-btn>
          </div>
        </v-flex>

        <v-flex xs12>
          <v-layout row justify-end>
            <v-btn to="/">Zurück</v-btn>
            <v-btn
              :disabled="!valid"
              color="primary"
              @click="submit"
            >
              Eintragen
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      homePlayerIds: [],
      awayPlayerIds: [],
      homeScore: undefined,
      awayScore: undefined,
      valid: true,
      sets: [],
    }
  },
  methods: {
    addSet() {
      this.sets.push({
        homePoints: 0,
        awayPoints: 0,
        homeColor: '',
        awayColor: '',
        homePositions: this.homePlayerIds.map(p => 'flexible'),
        awayPositions: this.awayPlayerIds.map(p => 'flexible'),
      })
    },
    removeSet(index) {
      this.sets = this.sets.filter((set, sIndex) => index != sIndex)
    },
    async submit() {
      if (!this.$refs.form.validate()) {
        return
      }

      await this.addMatchResult({
        homePlayers: this.homePlayerIds,
        awayPlayers: this.awayPlayerIds,
        homeScore: this.homeScore,
        awayScore: this.awayScore,
        sets: this.sets,
      })

      this.$router.push('/')
    },
    ...mapActions({
      addMatchResult: 'addMatchResult',
    })
  },
  watch: {
    sets: {
      deep: true,
      handler() {
        this.homeScore = this.sets.filter((s) => s.homePoints >= s.awayPoints).length
        this.awayScore = this.sets.filter((s) => s.homePoints <= s.awayPoints).length
        this.sets.forEach((set) => {
          if (set.homeColor == 'red') {
            set.awayColor = 'blue'
          }
          if (set.homeColor == 'blue') {
            set.awayColor = 'red'
          }
          if (set.awayColor == 'red') {
            set.homeColor = 'blue'
          }
          if (set.awayColor == 'blue') {
            set.homeColor = 'red'
          }
          if (this.homePlayerIds.length == 2) {
            if (set.homePositions[0] == 'attack') {
              set.homePositions[1] = 'defense'
            }
            if (set.homePositions[0] == 'defense') {
              set.homePositions[1] = 'attack'
            }
          }
          if (this.awayPlayerIds.length == 2) {
            if (set.awayPositions[0] == 'attack') {
              set.awayPositions[1] = 'defense'
            }
            if (set.awayPositions[0] == 'defense') {
              set.awayPositions[1] = 'attack'
            }
          }
        })
      },
    },
  },
  computed: {
    homePlayers() {
      return this.homePlayerIds.map(this.getPlayerById)
    },
    awayPlayers() {
      return this.awayPlayerIds.map(this.getPlayerById)
    },
    differentFromAwayPlayers() {
      return (ids) => !ids.some(id => this.awayPlayerIds.includes(id)) || 'Darf nicht in mehreren Teams auftauchen'
    },
    differentFromHomePlayers() {
      return (ids) => !ids.some(id => this.homePlayerIds.includes(id)) || 'Darf nicht in mehreren Teams auftauchen'
    },
    requiredArray() {
      return (ids) => ids.length > 0 || 'Darf nicht leer sein'
    },
    required() {
      return (input) => (input !== undefined && input !== '') || 'Pflichtfeld'
    },
    scoreRules() {
      return [
        this.required,
        (input) => input >= 0 || 'Darf nicht negativ sein',
      ]
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

<style scoped>
.my-auto {
  margin-top: auto;
  margin-bottom: auto;
}
</style>
