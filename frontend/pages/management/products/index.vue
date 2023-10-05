<template>
  <div class="products col-12 px-4 pb-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="mb-0 d-flex align-items-center">
        <n-icon class="me-2"> <CubeOutline /> </n-icon> Товары:
      </n-h1>
      <div class="action-block d-flex flex-wrap ms-auto">
        <PaginationComponent
          v-if="pagination.totalPages > 1"
          class="pe-4"
          :pagination="pagination"
          @update:page="handleUpdatePage"
        />
        <n-button color="#323232" @click="createProduct()">
          <template #icon>
            <n-icon>
              <add-outline />
            </n-icon>
          </template>
          Добавить товар
        </n-button>
      </div>
    </div>
    <ItemsTable
      :key="String($route.query?.page)"
      :columns="productsColumns()"
      :data="products"
    />
  </div>
</template>

<script lang="ts" setup>
import { AddOutline, CubeOutline } from '@vicons/ionicons5'
import type { getProductsInterface } from '~/interfaces/getProducts'

/// ///
// Components
const ItemsTable = defineAsyncComponent(
  () => import('~/components/ui/management/itemsTable.vue')
)

const PaginationComponent = defineAsyncComponent(
  () => import('~/components/ui/pages/PaginationComponent.vue')
)

/// ///
// Variables
const productsStore = storeProducts()
const categoriesStore = storeCategories()

const { products, pagination } = storeToRefs(productsStore)

const filters = ref<getProductsInterface>({
  all: true,
  ...$route().query
})

/// ///
// Functions
function createProduct() {
  $router().push('products/new')
}

function handleUpdatePage(number: number) {
  $router().push({ query: { page: number } })
  filters.value.page = number
  getProducts(unref(filters))
}

async function getProducts(filters: getProductsInterface) {
  await productsStore.getProducts(unref(filters))
}

await getProducts(unref(filters))
await categoriesStore.getCategories()
</script>
