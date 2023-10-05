<template>
  <div
    v-if="$route.params.id"
    id="edit-order"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <OrderComponent :id="String($route.params.id)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const OrderComponent = defineAsyncComponent(
  () => import('~/components/pages/management/orderComponent.vue')
)
</script>
