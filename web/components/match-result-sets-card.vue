<template>
  <match-result-card
    :teams="teams"
    :date="date"
  >
    <template slot="bottom">
      <ul class="match__sets">
        <li
          v-for="(set, index) in sets"
          :key="index"
          class="set"
        >
          <div class="set__container set__container--left">
            <i
              v-for="(_, i) in Array(set.home_points)"
              :key="index + '-' + i"
              class="set__point set__point--red"
            />
          </div>
          <div class="set__container set__container--right">
            <i
              v-for="(_, i) in Array(set.away_points)"
              :key="i"
              class="set__point set__point--blue"
            />
          </div>
        </li>
      </ul>
    </template>
  </match-result-card>
</template>

<script>
// TODO 1) build a separate card for matchmaking 2) combine this and the other card
import MatchResultCard from '~/components/match-result-card'

export default {
  components: {
    MatchResultCard,
  },
  props: {
    teams: {
      type: Array,
      required: true,
    },
    date: {
      type: String,
      required: false,
    },
    sets: {
      type: Array,
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.match__sets {
  list-style: none;
  padding: 0;
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
  font-size: initial;
  line-height: normal;
}

.set {
  display: flex;
  justify-content: center;
  margin-left: -75%;
  margin-right: -75%;
}

.set__container--left {
  width: 100%;
  text-align: right;
}

.set__container--right {
  width: 100%;
  text-align: left;
}

.set__point {
  display: inline-block;
  width: 0.75rem;
  height: 0.75rem;
  border-radius: 50%;
  margin-left: 1px;
  margin-right: 1px;
}

.set__point--red {
  background: #E53935;
}

.set__point--blue {
  background: #1976D2;
}
</style>

