<template>
  <v-card>
    <div class="matchresult">
      <div class="matchresult__team matchresult__team--left">
        <div
          v-for="player in homePlayers"
          :key="player.id"
        >
          {{ player.user.username }}
        </div>
        <v-icon
          v-if="homeScore > awayScore"
          class="matchresult__crown matchresult__crown--left"
        >mdi-crown</v-icon>
      </div>
      <div class="matchresult__meta">
        <slot name="center">
          <div class="matchresult__score matchresult__score--left">
            {{ homeScore }}
          </div>
          <div class="matchresult__score matchresult__score--center">
            :
          </div>
          <div class="matchresult__score matchresult__score--right">
            {{ awayScore }}
          </div>
          <div class="matchresult__date">
            {{ new Date(date).toLocaleDateString() }}
          </div>
        </slot>
        <slot name="bottom" />
      </div>
      <div class="matchresult__team matchresult__team--right">
        <div
          v-for="player in awayPlayers"
          :key="player.id"
        >
          {{ player.user.username }}
        </div>
        <v-icon
          v-if="homeScore < awayScore"
          class="matchresult__crown matchresult__crown--right"
        >mdi-crown</v-icon>
      </div>
    </div>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  props: {
    teams: {
      type: Array,
      required: true,
    },
    date: {
      type: String,
      required: false,
    },
  },
  computed: {
    homeScore() {
      return this.teams[0].score
    },
    awayScore() {
      return this.teams[1].score
    },
    homePlayers() {
      return this.teams[0].players.map(this.getPlayerById)
    },
    awayPlayers() {
      return this.teams[1].players.map(this.getPlayerById)
    },
    ...mapGetters({
      getPlayerById: 'getPlayerById',
    })
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
    font-size: x-large;
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

