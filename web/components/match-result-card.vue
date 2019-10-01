<template>
  <v-card>
    <div class="matchresult">
      <div class="matchresult__team matchresult__team--left">
        <div
          v-for="player in matchResult.home_players"
          :key="player.id"
        >
          {{ player.user.username }}
        </div>
        <v-icon
          v-if="matchResult.home_score > matchResult.away_score"
          class="matchresult__crown matchresult__crown--left"
        >mdi-crown</v-icon>
      </div>
      <div class="matchresult__meta">
        <div class="matchresult__score matchresult__score--left">
          {{ matchResult.home_score }}
        </div>
        <div class="matchresult__score matchresult__score--center">
          :
        </div>
        <div class="matchresult__score matchresult__score--right">
          {{ matchResult.away_score }}
        </div>
        <div class="matchresult__date">
          {{ new Date(matchResult.created).toLocaleDateString() }}
        </div>
      </div>
      <div class="matchresult__team matchresult__team--right">
        <div
          v-for="player in matchResult.away_players"
          :key="player.id"
        >
          {{ player.user.username }}
        </div>
        <v-icon
          v-if="matchResult.home_score < matchResult.away_score"
          class="matchresult__crown matchresult__crown--right"
        >mdi-crown</v-icon>
      </div>
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    matchResult: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
.matchresult {
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

