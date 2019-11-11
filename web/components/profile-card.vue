<template>
  <v-card v-if="loaded">
    <v-card-title primary-title>
      <h3 class="headline">
        {{ player.user.username }}
      </h3>
    </v-card-title>
    <v-container>
      <p>
        Siege: {{ stats.wins }} ({{ Math.floor(100 * stats.wins / stats.count) }}% Siegesrate)
      </p>
      <p>
        Tore: {{ stats.points }} ({{ (stats.points / stats.sets).toFixed(2) }} pro Satz)
      </p>
      <p>
        Wertung: {{ Math.floor(player.rating) }} TrueSkill
      </p>
      <ranking-scatter :ratings="ratings" />
    </v-container>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import RankingScatter from '~/components/ranking-scatter'

export default {
  components: {
    RankingScatter,
  },
  data() {
    return {
      loaded: false,
      ratings: [],
      player: {},
      stats: {},
    }
  },
  props: {
    id: {
      type: Number,
      required: true,
    },
  },
  async created() {
    const ratings = await this.$axios.$get('/match-players/?player.user.id=' + this.id)
    this.player = this.getPlayerById(this.id)
    this.ratings = [{ mu: this.player.rating_mu, sigma: this.player.rating_sigma }].concat(
      ratings.results.map((mp) => ({ mu: mp.rating_mu, sigma: mp.rating_sigma }))
    )
    this.stats = await this.$axios.$get('/players/' + this.id + '/stats/')
    this.loaded = true
  },
  computed: {
    ...mapGetters({
      'getPlayerById': 'getPlayerById',
    })
  },
}
</script>
