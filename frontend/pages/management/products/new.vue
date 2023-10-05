<template>
  <div
    id="new-product"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <ProductComponent />
  </div>
</template>

<script lang="ts" setup>
const ProductComponent = defineAsyncComponent(
  () => import('~/components/pages/management/productComponent.vue')
)
</script>
