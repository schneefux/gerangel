<template>
  <v-container>
    <h1 class="mb-3">Profil</h1>
    <v-card>
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
import RankingScatter from '~/components/ranking-scatter'

export default {
  components: {
    RankingScatter,
  },
  async asyncData({ params, $axios }) {
    const data = await $axios.$get('/match-players/?player.user.id=' + params.id)
    return {
      userRatings: data.results,
      player: data.results[0].player,
    }
  },
  computed: {
    ratings() {
      return [{ mu: this.player.rating_mu, sigma: this.player.rating_sigma }].concat(
        this.userRatings.map((mp) => ({ mu: mp.rating_mu, sigma: mp.rating_sigma }))
      )
    },
  },
}
</script>
