<template>
  <v-form>
    <v-container>
      <v-layout row wrap>
        <v-flex xs12>
          <v-text-field
            v-model="username"
            label="Benutzername"
            required
          ></v-text-field>
        </v-flex>

        <v-flex xs12>
          <v-text-field
            v-model="password"
            label="Passwort"
            type="password"
            required
          ></v-text-field>
        </v-flex>

        <v-flex>
          <v-layout justify-space-between>
            <v-btn
              :disabled="!isLoggedIn"
              @click="update"
            >
              Zugangsdaten ändern
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    async update() {
      const user = {
        id: this.user.id,
        ...this.username.length > 0 ? {
          username: this.username,
        } : {},
        ...this.password.length > 0 ? {
          password: this.password,
        } : {},
      }

      await this.updateUser(user)
    },
    ...mapActions({
      updateUser: 'updateUser',
    })
  },
  watch: {
    isLoggedIn(isLoggedIn) {
      if (isLoggedIn) {
        this.username = this.user.username
      }
    },
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'isLoggedIn',
    }),
    ...mapState({
      user: (state) => state.user,
    })
  },
}
</script>
