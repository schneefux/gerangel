<template>
  <div class="plotly" ref="graph" />
</template>

<script>
export default {
  props: {
    ratings: {
      type: Array,
      required: true,
    },
  },
  async mounted() {
    await this.refresh()
  },
  watch: {
    ratings: 'refresh',
  },
  methods: {
    refresh() {
      const traces = [-1, 0, +1].map((k, i) => ({
        // x: range len to 0
        x: [...Array(this.ratings.length).keys()].reverse(),
        y: this.ratings.map(({ mu, sigma }) => mu + k * sigma),
        line: { shape: 'line' },
        type: 'scatter',
        mode: 'lines',
        name: k == 0 ? '' : k + ' sigma',
        fill: i == 0 ? '' : 'tonexty',
        marker: {
          color: k == 0 ? this.$vuetify.theme.secondary : this.$vuetify.theme.primary,
        },
        line: {
          width: k == 0 ? 5 : 0,
        },
        fillcolor: this.$vuetify.theme.primary,
      }))
      console.log(this.$vuetify.theme.primary)

      this.plot = this.$plotly.newPlot(this.$refs.graph, traces, {
        xaxis: {
          title: 'Spiele',
          fixedrange: true,
        },
        yaxis: {
          title: 'TrueSkill',
          fixedrange: true,
        },
        showlegend: false,
        margin: { t: 40, l: 40, b: 40, r: 40 },
      }, {
        displayModeBar: false,
        responsive: true,
      })
    },
  },
}
</script>

<style scoped>
.plotly {
  height: 20em;
}
</style>
