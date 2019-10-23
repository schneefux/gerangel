<template>
  <v-container>
    <h1 class="mb-3">Profil</h1>
    <v-card v-if="isLoggedIn">
      <v-card-title primary-title>
        <h3 class="headline">
          {{ player.user.username }}
        </h3>
      </v-card-title>
      <v-container>
        <p>
          Wertung: {{ Math.floor(player.rating) }} TrueSkill
        </p>
        <v-sparkline
          :value="ratings"
          :labels="dates"
          padding="16"
        />
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  computed: {
    ratings() {
      return this.userRatings
        .map((matchPlayer) => matchPlayer.rating)
    },
    dates() {
      return this.userRatings
        .map((matchPlayer) => matchPlayer.team.match.created)
        .map((date) => new Date(Date.parse(date)).toLocaleDateString())
    },
    ...mapState({
      userRatings: (state) => state.userRatings,
    }),
    ...mapGetters({
      player: 'player',
      isLoggedIn: 'isLoggedIn',
    }),
  },
  watch: {
    async isLoggedIn(loggedIn) {
      if (loggedIn && this.userRatings.length == 0) {
        await this.loadUserRatings()
      }
    },
  },
  methods: {
    ...mapActions({
      loadUserRatings: 'loadUserRatings',
    })
  },
}
</script>
