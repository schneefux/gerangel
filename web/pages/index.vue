<template>
  <v-container fluid grid-list-md>
    <v-layout column items-center>
      <v-btn
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
        v-for="match in matches"
        :key="match.url"
        xs12
      >
        <v-layout justify-center>
          <v-flex xs12 sm6 md4 lg3>
            <match-card :match="match" />
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import MatchCard from '~/components/match-card'

export default {
  components: {
    MatchCard
  },
  computed: {
    ...mapState({
      matches: (state) => state.matches,
    })
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
    right: 0.25rem;
    font-size: large;
    color: goldenrod;
  }
}
</style>

