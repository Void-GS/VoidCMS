<template>
  <div
    id="product"
    class="navbar-compensation d-flex flex-wrap flex-grow-1 flex-md-nowrap"
  >
    <div
      class="categories-menu-container flex-column ms-4 ps-2 pt-3 d-none d-md-flex"
    >
      <div class="categories-menu slide-in-fwd-left-nodelay">
        <CategoriesMenu v-if="categories.length" :categories="categories" />
      </div>
    </div>
    <div class="product-info col pt-2 mt-1 pe-4 ps-4 ps-md-0 fade-in">
      <Breadcrumbs :breadcrumbs="breadcrumbs" class="mb-2 me-auto" />

      <ProductComponent v-if="product" :product="product" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { BreadcrumbInterface } from '~/interfaces/breadcrumb'

/// ///
// Components
const Breadcrumbs = defineAsyncComponent(
  () => import('~/components/ui/pages/BreadCrumbComponent.vue')
)
const CategoriesMenu = defineAsyncComponent(
  () => import('~/components/ui/pages/CategoriesMenuComponent.vue')
)
const ProductComponent = defineAsyncComponent(
  () => import('~/components/pages/product/ProductPageComponent.vue')
)

/// ///
// Variables
const params = $route().params

const productsStore = storeProducts()
const categoriesStore = storeCategories()
const { categoryByIdGetter } = storeToRefs(categoriesStore)

await productsStore.getProducts(params)
await categoriesStore.getCategories()

const breadcrumbs = computed<BreadcrumbInterface[]>(() => {
  return [
    {
      name: categoryByIdGetter.value(product.value?.category || 0)?.title,
      type: 'category',
      url: `/products/${
        categoryByIdGetter.value(product.value?.category || 0)?.meta_url
      }`
    },
    {
      name: product.value?.title,
      type: 'product',
      url: ''
    }
  ] as BreadcrumbInterface[]
})

const product = computed(() => {
  return productsStore.productByMetaGetter(String(params.meta_url))
})

const categories = computed(() => {
  return categoriesStore.categories
})

/// ///
// Meta
useSeoMeta(generateSeo(product.value!))
</script>
