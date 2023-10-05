<template>
  <div
    v-if="$route.params.id"
    id="edit-category"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <CategoryComponent :id="String($route.params.id)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const CategoryComponent = defineAsyncComponent(
  () => import('~/components/pages/management/categoryComponent.vue')
)
</script>
