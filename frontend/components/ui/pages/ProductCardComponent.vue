<template>
  <div class="product p-3">
    <n-card :bordered="false" :hoverable="true">
      <template #header>
        <div class="title-heading d-flex flex-column text-center">
          <n-text
            class="title d-flex align-items-center justify-content-center"
            strong
          >
            <nuxt-link :href="`/product/${product.meta_url}`">
              <n-ellipsis
                class="title-text text-uppercase"
                line-clamp="2"
                style="max-width: 280px"
              >
                {{ product.title }}
              </n-ellipsis>
            </nuxt-link>
          </n-text>
          <n-text class="price mt-1">{{ product.price }} РУБ.</n-text>
        </div>
      </template>
      <template #cover>
        <div
          class="action-panel d-flex flex-column align-items-center justify-content-center"
        >
          <div
            class="circled-icon d-flex align-items-center justify-content-center"
            @click="handleCart"
          >
            <n-icon size="22" color="white">
              <BagRemoveOutline v-if="isInCart(product.id!)" color="red" />
              <BagOutline v-else />
            </n-icon>
          </div>
          <div
            v-if="isAdmin"
            class="circled-icon d-flex align-items-center justify-content-center mt-2"
            @click="handleEdit(product.id!, '/management/products/edit/')"
          >
            <n-icon size="22" color="white" class="icon-button">
              <PencilOutline />
            </n-icon>
          </div>
        </div>
        <n-carousel v-if="product?.images?.length || 0 > 1" touchable>
          <n-image
            v-for="image in product.images"
            :key="image.id"
            class="product-image"
            object-fit="cover"
            preview-disabled
            height="320"
            :src="`${$config.public.media}${image?.url}`"
            :intersection-observer-options="{
              root: null,
              rootMargin: '250px',
              threshold: 0.1
            }"
            lazy
          />
          <template #dots="{ total, currentIndex, to }">
            <ul class="custom-dots">
              <li
                v-for="index of total"
                :key="index"
                :class="{ ['is-active']: currentIndex === index - 1 }"
                @click="to(index - 1)"
              />
            </ul>
          </template>
        </n-carousel>
        <div v-else class="product-single-image col">
          <n-image
            class="product-image in-card"
            object-fit="cover"
            preview-disabled
            height="320"
            :src="handleImageOrEmpty(product)"
            :intersection-observer-options="{
              root: null,
              rootMargin: '250px',
              threshold: 0.1
            }"
            lazy
          />
        </div>
      </template>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { BagOutline, BagRemoveOutline, PencilOutline } from '@vicons/ionicons5'
import type { ProductInterface } from '~/interfaces/product'

/// ///
// Props
const props = defineProps<{
  product: ProductInterface
}>()

const { isAdmin } = storeToRefs($auth())

/// ///
// Variables
const cartStore = storeCart()
const { isInCart } = cartStore

/// ///
// Functions
function handleCart() {
  const defaultComplectations = setDefaultComplectations(props.product)!
  const inCart = isInCart(props.product.id!)
  if (inCart) {
    cartStore.removeFromCart(props.product.id!)
  } else {
    cartStore.addToCart(props.product, defaultComplectations, 1)
  }
}
</script>

<style lang="scss" scoped>
.product {
  position: relative;
  max-width: 90vw;
  .action-panel {
    position: absolute;
    top: 1rem;
    right: 1rem;
    min-width: 50px;
    min-height: 50px;
    z-index: 1;
  }
  .title-heading {
    .title {
      height: 45px;
      cursor: pointer;
      line-height: 1.3;
      font-size: 0.9rem;
      font-weight: 600;
      letter-spacing: 0.1rem;
    }
    .price {
      font-weight: lighter;
      font-size: $font-size-small;
    }
  }
  .product-image {
    width: 100%;
  }
}

// Carousel
.custom-arrow {
  display: flex;
  position: absolute;
  bottom: 25px;
  right: 10px;
}

.custom-dots {
  display: flex;
  margin: 0;
  padding: 0;
  position: absolute;
  bottom: 20px;
  left: 20px;
}

.custom-dots li {
  display: inline-block;
  width: 16px;
  height: 8px;
  margin: 0 3px;
  box-shadow: rgba(50, 50, 93, 0.5) 0px 13px 27px -5px,
    rgba(0, 0, 0, 0.8) 0px 8px 16px -8px;
  border: 2px solid #fff;
  background-color: $background-glass-dark;
  transition: width 0.3s, background-color 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.custom-dots li.is-active {
  width: 40px;
  background: #fefefe;
}
</style>
