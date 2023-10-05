<template>
  <div class="orders col-12 px-4 pb-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="mb-0 d-flex align-items-center">
        <n-icon class="me-2"> <WalletOutline /> </n-icon> Заказы:
      </n-h1>
    </div>
    <ItemsTable
      :columns="ordersColumns()"
      :data="orders"
      :no-empty-action="true"
    />
  </div>
</template>

<script lang="ts" setup>
import { WalletOutline } from '@vicons/ionicons5'

/// ///
// Components
const ItemsTable = defineAsyncComponent(
  () => import('~/components/ui/management/itemsTable.vue')
)

/// ///
// Variables
const ordersStore = storeOrders()
const { orders } = storeToRefs(ordersStore)

onMounted(async () => {
  await ordersStore.getOrders(true)
})
</script>
