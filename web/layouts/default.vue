<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-side-icon @click="drawerOpen = !drawerOpen" />
      <v-toolbar-title>
        Gerangel [ɡəˈʁaŋl̩]
      </v-toolbar-title>
    </v-toolbar>

    <v-navigation-drawer
      v-model="drawerOpen"
      clipped
      fixed
      app
      width="300"
    >
      <v-list>
        <v-list-tile
          v-if="player == undefined"
          to="/login"
          nuxt
        >
          <v-list-tile-action>
            <v-icon>mdi-login</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            Einloggen
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile
          v-else
          @click="logout"
        >
          <v-list-tile-action>
            <v-icon>mdi-logout</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            Ausloggen ({{ player.user.username }})
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile
          to="/"
          nuxt
        >
          <v-list-tile-action>
            <v-icon>mdi-format-list-bulleted</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            Spielverlauf
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          to="/new-match"
          nuxt
        >
          <v-list-tile-action>
            <v-icon>mdi-plus</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            Spiel eintragen
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          to="/matchmake"
          nuxt
        >
          <v-list-tile-action>
            <v-icon>mdi-auto-fix</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            Matchmaking
          </v-list-tile-content>
        </v-list-tile>
        <v-list-tile
          to="/leaderboard"
          nuxt
        >
          <v-list-tile-action>
            <v-icon>mdi-trending-up</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            Rangliste
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>

    <v-footer>
      <v-layout justify-center row>
        <span>&copy; 2019 Gerangel Solutions</span>
      </v-layout>
    </v-footer>
  </v-app>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      drawerOpen: false,
    }
  },
  computed: {
    ...mapState({
      player: (state) => state.player,
    })
  },
  methods: {
    ...mapActions({
      logout: 'logout',
    })
  },
}
</script>
