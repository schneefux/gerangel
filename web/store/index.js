export const state = () => ({
  version: undefined, // persristed store schema version
  user: undefined, // logged in user
  token: '',
  matchResults: [],
  players: [],
  userRatings: [],
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
  setUserRatings(state, userRatings) {
    state.userRatings = userRatings
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
  async nuxtClientInit({ dispatch }) {
    // called by layout after vuex-persist has loaded the state
    await dispatch('loadUserRatings')
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
  async addMatchResult({ state, commit, dispatch }, matchResult) {
    const createdMatchResult = await this.$axios.$post('/match-results/', {
      home_players: matchResult.homePlayers,
      away_players: matchResult.awayPlayers,
      home_score: matchResult.homeScore,
      away_score: matchResult.awayScore,
    })
    commit('addMatchResult', joinMatchResults(state)(createdMatchResult))
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
  async loginUser({ state, commit, dispatch }, user) {
    const { token } = await this.$axios.$post('/login', user)
    const player = state.players.find((player) => player.user.username == user.username)
    commit('setUser', player.user)
    commit('setToken', token)
    this.$axios.setToken('Token ' + state.token)

    await dispatch('loadUserRatings')
  },
  logout({ commit }) {
    commit('setUser', undefined)
  },
  async loadUserRatings({ commit, state, getters }) {
    if (!getters.isLoggedIn) {
      return
    }

    const userRatings = await this.$axios.$get('/match-players/?player.user.id=' + state.user.id)
    commit('setUserRatings', userRatings.results)
  },
}
