<template>
  <v-container>
    <h1 class="mb-3">Profil</h1>
    <profile-card :id="id" />
  </v-container>
</template>

<script>
import ProfileCard from '~/components/profile-card'

export default {
  components: {
    ProfileCard,
  },
  async asyncData({ params }) {
    return {
      id: parseInt(params.id),
    }
  },
}
</script>
