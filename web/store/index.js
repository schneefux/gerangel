export const state = () => ({
  version: undefined, // persristed store schema version
  user: undefined, // logged in user
  token: '',
  matchResults: [],
  players: [],
})

export const getters = {
  isLoggedIn(state) {
    return state.user !== undefined
  },
  player(state, getters) {
    if (!getters.isLoggedIn) {
      return undefined
    }
    return state.players.find(
      (player) => player.user.id == state.user.id)
  },
  getPlayerById: (state) => (id) => {
    return state.players.find(player => player.id === id)
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
  setUser(state, user) {
    state.user = user
  },
  setToken(state, token) {
    state.token = token
  },
}

export const actions = {
  async nuxtServerInit({ dispatch }) {
    await dispatch('loadPlayers')
    await dispatch('loadMatchResults')
  },
  async nuxtClientInit({ dispatch }) {
    // called by layout after vuex-persist has loaded the state
  },
  async loadMatchResults({ state, commit }) {
    const data = await this.$axios.$get('/match-results/')
    const matchResults = data.results
    commit('setMatchResults', matchResults)
  },
  async loadPlayers({ commit }) {
    const data = await this.$axios.$get('/players/')
    commit('setPlayers', data.results)
  },
  async addMatchResult({ state, commit, dispatch }, matchResult) {
    const sets = matchResult.sets.map(set => ({
      home_points: set.homePoints,
      away_points: set.awayPoints,
      home_color: set.homeColor,
      away_color: set.awayColor,
      home_positions: set.homePositions,
      away_positions: set.awayPositions,
    }))
    const createdMatchResult = await this.$axios.$post('/match-results/', {
      teams: [{
        id: 'home',
        score: matchResult.homeScore,
        players: matchResult.homePlayers,
      }, {
        id: 'away',
        score: matchResult.awayScore,
        players: matchResult.awayPlayers,
      }],
      sets,
    })
    commit('addMatchResult')
    await dispatch('loadPlayers')
  },
  async registerUser({ dispatch, commit }, user) {
    const newUser = await this.$axios.$post('/users/', user)
    commit('setUser', newUser)
    await dispatch('loadPlayers')
    await dispatch('loginUser', user)
  },
  async updateUser({ dispatch, commit }, user) {
    const newUser = await this.$axios.$patch('/users/' + user.id + '/', user)
    commit('setUser', newUser)
    await dispatch('loadPlayers')
  },
  async loginUser({ state, commit }, user) {
    const { token } = await this.$axios.$post('/login', user)
    const player = state.players.find((player) => player.user.username == user.username)
    commit('setUser', player.user)
    commit('setToken', token)
    this.$axios.setToken('Token ' + state.token)
  },
  logout({ commit }) {
    commit('setUser', undefined)
  },
}
