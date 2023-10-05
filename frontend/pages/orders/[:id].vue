<template>
  <div
    id="order-id"
    class="navbar-compensation d-flex flex-grow-1 flex-column align-items-center p-4 pt-5"
  >
    <OrderPageComponent :order="orderById(orderId)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const OrderPageComponent = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageComponent.vue')
)

/// ///
// Variables
const ordersStore = storeOrders()
const { orderById } = storeToRefs(ordersStore)

const orderId = String($route().params.id)
await ordersStore.getOrderById(orderId)
</script>
