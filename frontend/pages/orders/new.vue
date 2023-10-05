<template>
  <div
    id="order"
    class="navbar-compensation d-flex flex-grow-1 flex-column align-items-center p-4 pt-5"
  >
    <OrderPageComponent />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const OrderPageComponent = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageComponent.vue')
)
</script>
