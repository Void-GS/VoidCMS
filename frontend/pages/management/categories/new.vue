<template>
  <div
    id="new-category"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <CategoryComponent />
  </div>
</template>

<script lang="ts" setup>
const CategoryComponent = defineAsyncComponent(
  () => import('~/components/pages/management/categoryComponent.vue')
)
</script>
