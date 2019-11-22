<template>
  <ul class="v-pagination v-pagination--circle theme--light">
    <li
      v-for="(_, i) in Array(max + 1)"
      :key="i"
      class=""
    >
      <button
        :class="{
          'v-pagination__item--active primary': i == value,
        }"
        class="v-pagination__item"
        @click.prevent="$emit('input', i)"
      >
        {{ i }}
      </button>
    </li>
  </ul>
</template>

<script>
// based on https://github.com/vuetifyjs/vuetify/blob/stable/packages/vuetify/src/components/VPagination/VPagination.ts
export default {
  props: {
    max: {
      // inclusive
      type: Number,
      default: 8,
    },
    value: {
      type: Number,
      required: true,
    }
  }
}
</script>
