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
        <ranking-scatter :ratings="ratings" />
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import RankingScatter from '~/components/ranking-scatter'

export default {
  components: {
    RankingScatter,
  },
  computed: {
    ratings() {
      return this.userRatings
        .map((mp) => ({ mu: mp.rating_mu, sigma: mp.rating_sigma }))
    },
    ...mapState({
      userRatings: (state) => state.userRatings,
    }),
    ...mapGetters({
      player: 'player',
      isLoggedIn: 'isLoggedIn',
    })
  },
}
</script>
