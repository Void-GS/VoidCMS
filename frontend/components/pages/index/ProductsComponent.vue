<template>
  <div id="products" class="p-md-4">
    <div class="products-title d-flex align-items-center mb-4 pb-4">
      <n-h2
        class="products-title-text text-nowrap d-flex align-items-center ms-4 mt-3"
      >
        <n-icon size="32" class="me-3" color="#FF5A00">
          <FlameOutline />
        </n-icon>
        Последние поступления
      </n-h2>
      <n-divider class="mx-4" />
    </div>
    <div class="products-container d-flex flex-wrap justify-content-center">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        class="col-12 col-md-12 col-lg-6 col-xl-3"
      />
    </div>
    <div
      class="products-show-all w-100 d-flex justify-content-center align-items-center mt-4 pt-4"
    >
      <n-divider class="mx-4" />

      <NuxtLink to="/products">
        <n-button size="large" round>
          <n-icon size="24" class="me-3">
            <CubeOutline />
          </n-icon>
          <strong v-text="'ВСЕ ТОВАРЫ'" />
        </n-button>
      </NuxtLink>
      <n-divider class="mx-4" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { CubeOutline, FlameOutline } from '@vicons/ionicons5'
import type { ProductInterface } from '~/interfaces/product'

defineProps<{
  products?: ProductInterface[]
}>()

/// ///
// Components
const ProductCard = defineAsyncComponent(
  () => import('~/components/ui/pages/ProductCardComponent.vue')
)
</script>
