export const state = () => ({
  player: undefined, // logged in player
  matches: [],
  players: [],
})

export const getters = {
}

export const mutations = {
  setMatches(state, matches) {
    state.matches = matches
  },
  addMatch(state, match) {
    state.matches = [match].concat(...state.matches)
  },
  setPlayers(state, players) {
    state.players = players
  },
  addPlayer(state, player) {
    state.players = state.players.concat(player)
  },
  setPlayer(state, player) {
    state.player = player
  },
}

export const actions = {
  async nuxtServerInit({ dispatch }) {
    await dispatch('loadPlayers')
    await dispatch('loadMatches')
  },
  async loadMatches({ state, commit }) {
    const data = await this.$axios.$get('/matches')
    const matches = data.results.map((match) => ({
      ...match,
      home_player: state.players.find(({ url }) => url == match.home_player),
      away_player: state.players.find(({ url }) => url == match.away_player),
    }))
    commit('setMatches', matches)
  },
  async loadPlayers({ commit }) {
    const data = await this.$axios.$get('/players')
    commit('setPlayers', data.results)
  },
  async addMatch({ state, commit }, match) {
    match = await this.$axios.$post('/matches/', match)
    match = {
      ...match,
      home_player: state.players.find(({ url }) => url == match.home_player),
      away_player: state.players.find(({ url }) => url == match.away_player),
    }

    commit('addMatch', match)
  },
  async registerUser({ commit }, user) {
    const data = await this.$axios.$post('/players/', user)
    commit('addPlayer', data)
    commit('setPlayer', data)
  },
  async loginUser({ state, commit }, user) {
    const data = state.players.find((player) => player.user.username == user.username)
    commit('setPlayer', data)
  },
}
