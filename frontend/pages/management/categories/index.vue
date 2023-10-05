<template>
  <div class="categories d-flex flex-column col-12 px-4 pb-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="mb-0 d-flex align-items-center">
        <n-icon class="me-2"> <LibraryOutline /> </n-icon> Категории:
      </n-h1>
      <n-button
        color="#323232"
        class="ms-auto btn-collapsing"
        @click="createCategory()"
      >
        <template #icon>
          <n-icon>
            <add-outline />
          </n-icon>
        </template>
        <span class="d-none d-md-block ms-2"> Добавить категорию </span>
      </n-button>
    </div>
    <DragTable
      v-if="categories.length"
      :items="categories"
      class="my-4"
      edit-path="/management/categories/edit/"
      @delete="categoriesStore.deleteCategory({ id: $event })"
      @move="onMove"
    />
    <div
      v-else
      class="empty flex-grow-1 d-flex justify-content-center align-items-center"
    >
      <n-empty size="huge" description="Нет доступных категорий">
        <template #extra>
          <NuxtLink to="categories/new">
            <n-button size="large"> Добавить категорию </n-button>
          </NuxtLink>
        </template>
      </n-empty>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { AddOutline, LibraryOutline } from '@vicons/ionicons5'

/// ///
// Components
const DragTable = defineAsyncComponent(
  () => import('~/components/ui/management/draggableTable.vue')
)

/// ///
// Variables
const categoriesStore = storeCategories()
const { categories } = storeToRefs(categoriesStore)

await categoriesStore.getCategories()

/// ///
// Functions
function createCategory() {
  $router().push('categories/new')
}

async function onMove(evt: Record<string, any>) {
  await categoriesStore.updateCategoryPosition({
    id: evt.item.id,
    parent_id: evt.to.id,
    position: evt.newIndex
  })
  categoriesStore.getCategories()
}
</script>
