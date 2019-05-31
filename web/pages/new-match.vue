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
              <v-select
                v-model="homePlayer"
                :items="players"
                :rules="[required, differentFromAwayPlayer]"
                item-text="user.username"
                item-value="url"
                label="Spieler"
              ></v-select>
            </v-flex>
            <v-flex xs3>
              <v-text-field
                v-model="homeScore"
                :rules="scoreRules"
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
              <v-select
                v-model="awayPlayer"
                :items="players"
                :rules="[required, differentFromHomePlayer]"
                item-text="user.username"
                item-value="url"
                label="Spieler"
              ></v-select>
            </v-flex>
            <v-flex xs3>
              <v-text-field
                v-model="awayScore"
                :rules="scoreRules"
                label="Punkte"
                type="number"
                required
              ></v-text-field>
            </v-flex>
          </v-layout>
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
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      homePlayer: undefined,
      awayPlayer: undefined,
      homeScore: undefined,
      awayScore: undefined,
      valid: true,
    }
  },
  methods: {
    async submit() {
      if (!this.$refs.form.validate()) {
        return
      }

      const match = {
        in_progress: false,
        home_player: this.homePlayer,
        away_player: this.awayPlayer,
        home_score: this.homeScore,
        away_score: this.awayScore,
      }

      await this.addMatch(match)
      this.$router.push('/')
    },
    ...mapActions({
      addMatch: 'addMatch',
    })
  },
  computed: {
    differentFromAwayPlayer() {
      return (player) => this.awayPlayer != player || 'Darf nicht gleich sein'
    },
    differentFromHomePlayer() {
      return (player) => this.homePlayer != player || 'Darf nicht gleich sein'
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
    ...mapState({
      players: (state) => state.players,
    })
  },
}
</script>
