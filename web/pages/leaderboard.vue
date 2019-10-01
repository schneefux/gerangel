<template>
  <v-container fluid grid-list-md>
    <v-layout column items-center>
      <h1>Rangliste</h1>
      <v-flex
        v-for="player in sortedPlayers"
        :key="player.id"
        xs12
      >
        <v-card>
          <v-card-title primary-title>
            <div>
              <div class="headline">{{ player.user.username }}</div>
              <span>{{ Math.floor(rating(player)) }} TrueSkill</span>
            </div>
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

function rating(player) {
  return player.rating_mu - 1.96 * player.rating_sigma
}

export default {
  data() {
    return {
      rating,
    }
  },
  computed: {
    sortedPlayers() {
      return this.players
        .concat()
        .sort((p1, p2) => rating(p2) - rating(p1))
    },
    ...mapState({
      players: (state) => state.players,
    })
  },
}
</script>
