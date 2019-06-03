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

/**
 * Replace references by objects
 */
function joinMatch(state) {
  return (match) => ({
    ...match,
    home_players: match.home_players.map((fUrl) => state.players.find(({ url }) => url == fUrl)),
    away_players: match.away_players.map((fUrl) => state.players.find(({ url }) => url == fUrl)),
  })
}

export const actions = {
  async nuxtServerInit({ dispatch }) {
    await dispatch('loadPlayers')
    await dispatch('loadMatches')
  },
  async loadMatches({ state, commit }) {
    const data = await this.$axios.$get('/matches')
    const matches = data.results.map(joinMatch(state))
    commit('setMatches', matches)
  },
  async loadPlayers({ commit }) {
    const data = await this.$axios.$get('/players')
    commit('setPlayers', data.results)
  },
  async addMatch({ state, commit }, match) {
    match = await this.$axios.$post('/matches/', match)
    match = joinMatch(state)(match)
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
