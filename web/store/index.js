export const state = () => ({
  player: undefined, // logged in player
  token: '',
  matchResults: [],
  players: [],
})

export const getters = {
  isLoggedIn(state) {
    return state.player !== undefined
  },
}

export const mutations = {
  setMatchResults(state, matchResult) {
    state.matchResults = matchResult
  },
  addMatchResult(state, matchResult) {
    state.matchResults = [matchResult].concat(...state.matchResults)
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
  setToken(state, token) {
    state.token = token
  },
}

/**
 * Replace references by objects
 */
function joinMatchResults(state) {
  return (matchResults) => ({
    ...matchResults,
    home_players: matchResults.home_players.map(fId => state.players.find(({ id }) => id == fId)),
    away_players: matchResults.away_players.map(fId => state.players.find(({ id }) => id == fId)),
  })
}

export const actions = {
  async nuxtServerInit({ dispatch }) {
    await dispatch('loadPlayers')
    await dispatch('loadMatchResults')
  },
  async loadMatchResults({ state, commit }) {
    const data = await this.$axios.$get('/match-results/')
    const matchResults = data.results.map(joinMatchResults(state))
    commit('setMatchResults', matchResults)
  },
  async loadPlayers({ commit }) {
    const data = await this.$axios.$get('/players/')
    commit('setPlayers', data.results)
  },
  async addMatchResult({ state, commit }, matchResult) {
    const createdMatchResult = await this.$axios.$post('/match-results/', {
      home_players: matchResult.homePlayers,
      away_players: matchResult.awayPlayers,
      home_score: matchResult.homeScore,
      away_score: matchResult.awayScore,
    })
    commit('addMatchResult', joinMatchResults(state)(createdMatchResult))
  },
  async registerUser({ commit }, user) {
    const createdUser = await this.$axios.$post('/users/', user)
    const player = await this.$axios.$get(`/players/?user.id=${createdUser.id}`)
    commit('addPlayer', player.results[0])
  },
  async loginUser({ state, commit }, user) {
    const { token } = await this.$axios.$post('/login', user)
    const player = state.players.find((player) => player.user.username == user.username)
    commit('setPlayer', player)
    commit('setToken', token)
    this.$axios.setToken('Token ' + token)
  },
}
