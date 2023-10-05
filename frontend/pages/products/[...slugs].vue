<template>
  <div class="products-page-container navbar-compensation flex-grow-1">
    <ProductsPageHeadComponent :category="category" class="puff-in-center" />
    <div
      id="products-page"
      class="d-flex flex-wrap flex-md-nowrap py-4 pe-4 ps-4 ps-md-0 slide-in-fwd-top"
    >
      <div
        class="categories-menu-container sticky-top d-flex flex-column ms-4 ps-2 d-md-flex"
      >
        <div class="categories-menu">
          <CategoriesMenu
            v-if="categories.length"
            :categories="categories"
            class="pt-1"
          />
        </div>
      </div>
      <div class="products-page-container w-100">
        <div
          class="products-page-filters d-flex flex-wrap flex-lg-nowrap align-items-center pb-3"
        >
          <Breadcrumbs :breadcrumbs="breadcrumbs" class="me-auto" />
          <FiltersComponent
            v-if="categoriesStore.categories.length"
            class="ps-2 pt-2 pt-md-1"
            :categories="categoriesStore.categories"
          />
        </div>
        <div
          id="products"
          class="products-page-products d-flex flex-wrap justify-content-start"
        >
          <div
            v-if="!products.length"
            class="empty w-100 full-height d-flex align-items-center justify-content-center"
          >
            <n-empty size="large" description="В данной категории нет товаров">
            </n-empty>
          </div>
          <ProductCard
            v-for="product in products"
            :key="product.id"
            :product="product"
            class="col-12 col-md-12 col-lg-6 col-xl-3"
          />
        </div>
      </div>
    </div>
    <PaginationComponent
      v-if="pagination.totalPages > 1"
      class="mt-4 w-100 justify-content-center"
      :pagination="pagination"
      @update:page="handleUpdatePage"
    />
  </div>
</template>

<script lang="ts" setup>
import type { BreadcrumbInterface } from '~/interfaces/breadcrumb'
import type { getProductsInterface } from '~/interfaces/getProducts'
import type { CategoryInterface } from '~/interfaces/category'

/// ///
// Components
const ProductsPageHeadComponent = defineAsyncComponent(
  () => import('~/components/pages/products/ProductsPageHeadComponent.vue')
)
/// ///
// Components
const Breadcrumbs = defineAsyncComponent(
  () => import('~/components/ui/pages/BreadCrumbComponent.vue')
)
const CategoriesMenu = defineAsyncComponent(
  () => import('~/components/ui/pages/CategoriesMenuComponent.vue')
)
const ProductCard = defineAsyncComponent(
  () => import('~/components/ui/pages/ProductCardComponent.vue')
)
const FiltersComponent = defineAsyncComponent(
  () => import('~/components/ui/pages/FiltersComponent.vue')
)
const PaginationComponent = defineAsyncComponent(
  () => import('~/components/ui/pages/PaginationComponent.vue')
)

/// ///
// Variables
const slugs = parseRouteProductsSlugs($route().params.slugs as [])

const filters = ref<getProductsInterface>({
  ...slugs
})

const productsStore = storeProducts()
const categoriesStore = storeCategories()

await categoriesStore.getCategories()

const { categories, categoryByMetaGetter } = storeToRefs(categoriesStore)
const { pagination, products } = storeToRefs(productsStore)

const category: CategoryInterface = categoryByMetaGetter.value(
  filters.value.category_url!
)!

const breadcrumbs = computed<BreadcrumbInterface[]>(() => {
  return [
    {
      name: 'Товары',
      type: 'product',
      url: '/products'
    },
    {
      name: categoryByMetaGetter.value(filters.value.category_url!)?.title,
      type: 'category',
      url: ''
    }
  ] as BreadcrumbInterface[]
})

/// ///
// Functions
function handleUpdatePage(number: number) {
  slugs.page = String(number)
  const routeSlugs = Object.values(slugs)
  $router().push({ params: { slugs: routeSlugs } })
}

async function getProducts(filters: getProductsInterface) {
  await productsStore.getProducts(unref(filters))
}

watch(
  () => $route().query,
  (newValue) => {
    getProducts(Object.assign({ ...unref(filters) }, { ...newValue }))
  }
)

onMounted(async () => {
  await getProducts(unref(filters))
})

/// ///
// Meta
useSeoMeta(
  generateSeo(
    categoriesStore.categoryByMetaGetter(filters.value.category_url!) || {}
  )
)
</script>

<style lang="scss" scoped>
.empty {
  height: 360px;
}
.products-page-filters {
  position: sticky;
  background: white;
  top: calc($navbar-height + 1rem);
  z-index: 2;
  &::before {
    position: absolute;
    content: '';
    bottom: 0;
    left: 0;
    background: white;
    width: 100%;
    height: 300px;
    z-index: -1;
  }
  @media (max-width: 768px) {
    top: calc($navbar-height + 0.6rem);
  }
}
</style>
