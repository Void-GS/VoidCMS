<template>
  <div id="filters" class="d-flex align-items-center d-none d-md-flex">
    <div class="filters-container">
      <div class="filter-price d-flex flex-wrap align-items-center">
        <strong class="me-4" v-text="'ЦЕНА:'" />
        <div
          class="price-item text-nowrap me-2"
          @click="updateQuery({ sort_price: 'desc' })"
          v-text="'ПО УБЫВАНИЮ'"
        />
        |
        <div
          class="price-item text-nowrap ms-2"
          @click="updateQuery({ sort_price: 'asc' })"
          v-text="'ПО ВОЗРАСТАНИЮ'"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { FiltersInterface } from '~/interfaces/filters'

/// ///
// Functions
function updateQuery(filters: FiltersInterface) {
  $router().replace({
    query: { ...$route().query, ...filters }
  })
}
</script>

<style lang="scss" scoped>
#filters {
  position: relative;
}
.price-item {
  cursor: pointer;
  user-select: none;
}
</style>
