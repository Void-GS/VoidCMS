<template>
  <div
    id="orders"
    class="navbar-compensation d-flex flex-column flex-grow-1 justify-content-center align-items-center p-4"
  >
    <template v-if="orders.length">
      <n-h1 class="mb-0">Офомленные заказы:</n-h1>
      <div class="orders-list d-flex flex-column align-items-center w-100">
        <OrderPageComponent
          v-for="order in orders"
          :key="order.id"
          class="mt-5"
          :order="order"
        />
      </div>
    </template>

    <template v-else>
      <n-empty size="huge" description="У вас еще не было заказов">
        <template #extra>
          <NuxtLink to="/products">
            <n-button size="small">Добавьте товары</n-button>
          </NuxtLink>
        </template>
      </n-empty>
    </template>
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

const { orders } = storeToRefs(ordersStore)
await ordersStore.getOrders()
</script>
