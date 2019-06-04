<template>
  <v-card>
    <div class="match">
      <div class="match__team match__team--left">
        <div
          v-for="player in match.home_players"
          :key="player.url"
        >
          {{ player.user.username }}
        </div>
        <v-icon
          v-if="match.home_score > match.away_score"
          class="match__crown match__crown--left"
        >mdi-crown</v-icon>
      </div>
      <div class="match__meta">
        <div class="match__score match__score--left">
          {{ match.home_score }}
        </div>
        <div class="match__score match__score--center">
          :
        </div>
        <div class="match__score match__score--right">
          {{ match.away_score }}
        </div>
        <div class="match__date">
          {{ new Date(match.created).toLocaleDateString() }}
        </div>
      </div>
      <div class="match__team match__team--right">
        <div
          v-for="player in match.away_players"
          :key="player.url"
        >
          {{ player.user.username }}
        </div>
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

  // team 30% + meta 20% + team 30% = 100%
  &__team {
    width: 30%;
    font-size: x-large;

    &--left {
      text-align: left;
    }

    &--right {
      text-align: right;
    }
  }

  &__meta {
    width: 40%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }

  &__score {
    font-size: xx-large;

    &--left {
      width: 40%;
      text-align: right;
    }
    &--center {
      width: 10%;
      text-align: center;
    }
    &--right {
      width: 40%;
      text-align: left;
    }
  }

  &__date {
    width: 100%;
    text-align: center;
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

