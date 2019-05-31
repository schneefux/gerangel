<template>
  <v-form
    v-model="valid"
    ref="form"
    lazy-validation
  >
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
              :disabled="!valid"
              @click="register"
            >
              Registrieren
            </v-btn>
            <v-btn
              :disabled="!valid"
              color="primary"
              @click="login"
            >
              Einloggen
            </v-btn>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-container>
  </v-form>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      valid: true,
      username: '',
      password: '',
    }
  },
  methods: {
    async register() {
      if (!this.$refs.form.validate()) {
        return
      }

      const user = {
        username: this.username,
        password: this.password,
      }

      await this.registerUser(user)
      this.$router.push('/')
    },
    async login() {
      if (!this.$refs.form.validate()) {
        return
      }

      const user = {
        username: this.username,
        password: this.password,
      }

      await this.loginUser(user)
      this.$router.push('/')
    },
    ...mapActions({
      loginUser: 'loginUser',
      registerUser: 'registerUser',
    })
  },
}
</script>
