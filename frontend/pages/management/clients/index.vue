<template>
  <div class="clients col-12 px-4 pb-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="mb-0 d-flex align-items-center">
        <n-icon class="me-2"> <PeopleOutline /> </n-icon> Клиенты:
      </n-h1>
    </div>
    <ItemsTable :columns="clientsColumns()" :data="clients" />
  </div>
</template>

<script lang="ts" setup>
import { PeopleOutline } from '@vicons/ionicons5'

/// ///
// Components
const ItemsTable = defineAsyncComponent(
  () => import('~/components/ui/management/itemsTable.vue')
)

/// ///
// Variables
const clientsStore = storeClients()
const { clients } = storeToRefs(clientsStore)

/// ///
// Functions

onMounted(async () => {
  await clientsStore.getClients()
})
</script>
