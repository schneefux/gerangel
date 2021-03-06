import VuexPersistence from 'vuex-persist'

export default ({ store, $axios }) => {
  window.onNuxtReady(() => new VuexPersistence({
    key: 'gerangel',
    reducer: state => ({
      version: state.version,
      user: state.user,
      token: state.token,
    }),
    restoreState: (key, storage) => {
      // pass through (https://github.com/championswimmer/vuex-persist/blob/master/src/index.ts#L189)
      let value = (storage).getItem(key)
      value = typeof value === 'string' ? JSON.parse(value || '{}') : (value || {})

      if (value.token) {
        $axios.setToken('Token ' + value.token)
      }

      value.version = 1

      return value
    }
  }).plugin(store))
}
