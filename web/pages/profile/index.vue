<template>
  <v-container>
    <h1 class="mb-3">Profil</h1>
    <profile-card
      v-if="isLoggedIn"
      :id="player.id"
    />
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import ProfileCard from '~/components/profile-card'

export default {
  components: {
    ProfileCard,
  },
  computed: {
    ...mapGetters({
      player: 'player',
      isLoggedIn: 'isLoggedIn',
    })
  },
}
</script>
