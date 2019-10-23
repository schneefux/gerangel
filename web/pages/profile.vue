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
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      player: 'player',
      isLoggedIn: 'isLoggedIn',
    }),
  },
}
</script>
