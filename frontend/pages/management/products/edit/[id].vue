<template>
  <div
    v-if="$route.params.id"
    id="edit-product"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <ProductComponent :id="String($route.params.id)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const ProductComponent = defineAsyncComponent(
  () => import('~/components/pages/management/productComponent.vue')
)
</script>
