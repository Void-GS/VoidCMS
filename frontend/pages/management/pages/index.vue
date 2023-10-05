<template>
  <div class="pages col-12 px-4 pb-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="mb-0 d-flex align-items-center">
        <n-icon class="me-2"> <DocumentTextOutline /> </n-icon> Страницы:
      </n-h1>
      <n-button color="#323232" class="ms-auto" @click="createPage()">
        <template #icon>
          <n-icon>
            <add-outline />
          </n-icon>
        </template>
        Добавить страницу
      </n-button>
    </div>
    <ItemsTable :columns="pagesColumns()" :data="pages" />
  </div>
</template>

<script lang="ts" setup>
import { AddOutline, DocumentTextOutline } from '@vicons/ionicons5'

/// ///
// Components
const ItemsTable = defineAsyncComponent(
  () => import('~/components/ui/management/itemsTable.vue')
)

/// ///
// Variables
const pagesStore = storePages()
const { pages } = storeToRefs(pagesStore)

/// ///
// Functions
function createPage() {
  $router().push('pages/new')
}

onMounted(async () => {
  await pagesStore.getPages({ all: true })
})
</script>
