<template>
  <v-card>
    <div class="match">
      <div class="match__team">
        {{ match.home_player.user.username }}
        <v-icon
          v-if="match.home_score > match.away_score"
          class="match__crown match__crown--left"
        >mdi-crown</v-icon>
      </div>
      <div class="match__score">
        {{ match.home_score }}
        :
        {{ match.away_score }}
      </div>
      <div class="match__team">
        {{ match.home_player.user.username }}
        <v-icon
          v-if="match.home_score < match.away_score"
          class="match__crown match__crown--right"
        >mdi-crown</v-icon>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    match: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
.match {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-left: 1rem;
  margin-right: 1rem;
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;

  &__team {
    font-size: x-large;
  }

  &__score {
    font-size: xx-large;
  }

  &__crown {
    position: absolute;
    top: 0;
    font-size: large;
    color: goldenrod;

    &--left {
      left: 0.25rem;
    }

    &--right {
      right: 0.25rem;
    }
  }
}
</style>

