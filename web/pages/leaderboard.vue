<template>
  <v-container fluid grid-list-md>
    <h1>Rangliste</h1>
    <v-data-table
      :headers="[
        { text: 'Rang', value: 'rank' },
        { text: 'Benutzername', value: 'name', sortable: false },
        { text: 'TrueSkill-Wertung', value: 'rating' }
      ]"
      :rows-per-page-items="[10, 50, 100]"
      :items="tablePlayers"
      must-sort
      class="elevation-1"
    >
      <template v-slot:items="props">
        <td>{{ props.item.rank }}</td>
        <td>{{ props.item.name }}</td>
        <td>{{ Math.floor(props.item.rating) }}</td>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'

export default {
  computed: {
    tablePlayers() {
      return this.players
        .concat()
        .sort((p1, p2) => p2.rating - p1.rating)
        .map((player, index) => ({
          rank: index + 1,
          rating: player.rating,
          name: player.user.username,
        }))
    },
    ...mapState({
      players: (state) => state.players,
    })
  },
}
</script>
