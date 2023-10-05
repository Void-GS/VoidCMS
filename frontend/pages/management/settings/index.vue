<template>
  <div class="settings col-12 pb-4 px-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="mb-0 d-flex align-items-center">
        <n-icon class="me-2"> <ConstructOutline /> </n-icon> Настройки:
      </n-h1>
      <n-button color="#323232" class="ms-auto" @click="createSettings()">
        <template #icon>
          <n-icon>
            <add-outline />
          </n-icon>
        </template>
        Добавить настройки домена
      </n-button>
    </div>
    <ItemsTable :columns="settingsColumns()" :data="settings" />
  </div>
</template>

<script lang="ts" setup>
import { AddOutline, ConstructOutline } from '@vicons/ionicons5'

/// ///
// Components
const ItemsTable = defineAsyncComponent(
  () => import('~/components/ui/management/itemsTable.vue')
)

/// ///
// Variables
const settingsStore = storeSettings()
const { settings } = storeToRefs(settingsStore)

/// ///
// Functions
function createSettings() {
  $router().push('settings/new')
}

onMounted(async () => {
  await settingsStore.getSettings()
})
</script>
