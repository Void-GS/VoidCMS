<template>
  <div class="search-item d-flex align-items-center">
    <div
      class="search-item-image pe-2"
      :class="{ 'col-3': category?.id, 'col-2': product?.id }"
    >
      <n-image
        object-fit="cover"
        class="in-card w-100"
        preview-disabled
        :src="`${handleImageOrEmpty(product || category)}`"
      />
    </div>
    <NuxtLink
      :to="getUrl()"
      class="search-item-info d-flex align-items-center flex-wrap col"
      @click="toggleShowSearch"
    >
      <div class="search-item-shared-info сol">
        <n-h5 class="search-item-title text-uppercase mb-0">
          <n-ellipsis style="max-width: 240px">
            {{ category?.title || product?.title }}
          </n-ellipsis>
        </n-h5>
        <n-text class="search-item-description">
          <n-ellipsis style="max-width: 240px" :tooltip="false">
            {{ category?.description || sanitizeText(product?.content!) }}
          </n-ellipsis>
        </n-text>
      </div>
      <div v-if="product?.id" class="search-item-price text-nowrap ms-auto">
        <n-text>Цена: <strong v-text="product.price" /> ₽</n-text>
      </div>
    </NuxtLink>
  </div>
</template>

<script lang="ts" setup>
import type { CategoryInterface } from '~/interfaces/category'
import type { ProductInterface } from '~/interfaces/product'

/// ///
// Props
const props = defineProps<{
  product?: ProductInterface
  category?: CategoryInterface
}>()

/// ///
// Emits
const emit = defineEmits(['update'])

/// ///
// Functions
function getUrl() {
  return props.product?.id
    ? `/product/${props.product.meta_url}`
    : `/products/${props.category?.meta_url}`
}
function toggleShowSearch() {
  setTimeout(() => {
    emit('update')
  }, 500)
}
</script>

<style lang="scss" scoped>
.search-item-image {
  height: 50px;
}
</style>
