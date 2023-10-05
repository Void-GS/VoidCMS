<template>
  <div id="index">
    <Header :categories="categories" :is-hidden="isHidden" />
    <Categories v-if="randomCategories.length" :categories="randomCategories" />
    <Products v-if="products.length" :products="products" />
  </div>
</template>

<script lang="ts" setup>
import type { CategoryInterface } from '~/interfaces/category'

/// ///
// Components
const Header = defineAsyncComponent(
  () => import('~/components/pages/index/HeaderComponent.vue')
)
const Categories = defineAsyncComponent(
  () => import('~/components/pages/index/CategoriesComponent.vue')
)
const Products = defineAsyncComponent(
  () => import('~/components/pages/index/ProductsComponent.vue')
)

/// ///
// Variables
const productsStore = storeProducts()
const categoriesStore = storeCategories()

await categoriesStore.getCategories()

const { products } = storeToRefs(productsStore)
const { categories, categoryGetRandomGetter } = storeToRefs(categoriesStore)

const randomCategories = ref<CategoryInterface[]>([])

const isHidden = ref<boolean>(false)

onMounted(async () => {
  randomCategories.value = [...categoryGetRandomGetter.value]
  await productsStore.getProducts()
})

/// ///
// Meta
useSeoMeta(generateSeo({}))
</script>
