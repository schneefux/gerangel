<template>
  <v-container fluid grid-list-md>
    <v-layout column items-center>
      <v-btn
        v-show="isLoggedIn"
        color="primary"
        to="/new-match"
        nuxt
        fixed
        bottom
        right
        fab
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>

      <v-flex
        v-for="matchResult in matchResults"
        :key="matchResult.id"
        xs12
      >
        <v-layout justify-center>
          <v-flex xs12 sm6 md4 lg3>
            <match-result-sets-card
              :teams="matchResult.teams"
              :date="matchResult.created"
              :sets="matchResult.sets"
            />
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
import MatchResultSetsCard from '~/components/match-result-sets-card'

export default {
  components: {
    MatchResultSetsCard
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'isLoggedIn',
    }),
    ...mapState({
      matchResults: (state) => state.matchResults,
    })
  },
}
</script>

<style lang="scss" scoped>
</style>

