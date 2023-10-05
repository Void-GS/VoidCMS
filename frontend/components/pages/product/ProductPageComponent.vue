<template>
  <div
    class="product-page-component w-100 d-flex flex-wrap flex-xl-nowrap justify-content-center pb-4"
  >
    <div
      class="product-page-images d-flex flex-wrap justify-content-center col"
    >
      <div class="image-container w-100">
        <n-image
          class="image in-card"
          height="460"
          object-fit="cover"
          :src="
            product.images?.length
              ? `${$config.public.media}${coverImage.url}`
              : handleImageOrEmpty(product)
          "
        />
      </div>
      <n-divider class="my-4" />
      <div
        v-if="product?.images?.length! > 1"
        class="carousel-container d-flex align-items-center"
      >
        <n-carousel
          effect="card"
          prev-slide-style="transform: translateX(-150%) translateZ(-800px);"
          next-slide-style="transform: translateX(50%) translateZ(-800px);"
          :show-dots="false"
          :on-update:current-index="setCoverImage"
        >
          <n-carousel-item
            v-for="img in product?.images"
            :key="img.id"
            class="carousel-item d-flex align-items-center justify-content-center"
          >
            <n-image
              preview-disabled
              class="caruosel-image"
              object-fit="cover"
              :src="`${$config.public.media}${img.url}`"
            />
          </n-carousel-item>
        </n-carousel>
      </div>
    </div>
    <div class="product-page-info ps-md-4 col-xl-6">
      <n-h3 class="product-title d-flex align-items-center mb-1">
        {{ product?.title }}

        <n-icon
          v-if="isAdmin"
          class="ms-2 icon-button"
          :size="22"
          @click="handleEdit(product?.id!, '/management/products/edit/')"
        >
          <PencilOutline />
        </n-icon>
      </n-h3>
      <n-h4 class="product-price my-0">
        <n-number-animation
          :from="calculatedPrice / 2"
          :duration="500"
          :to="calculatedPrice"
          :active="true"
          :precision="2"
        />
        РУБ.</n-h4
      >
      <div
        v-if="product.complectations"
        class="product-complectations d-flex align-items-center justify-content-start col-12 mt-3"
      >
        <ComplectationSelector
          :complectations-prop="product.complectations"
          @update="handleAssignComplectations"
        />
      </div>
      <n-divider />
      <n-text>
        <strong class="mb-4" v-text="'Описание:'" />
        <div class="product-info" v-html="product?.content" />
      </n-text>
      <n-divider class="my-4" />
      <div class="d-flex flex-wrap justify-content-end">
        <div class="items-count w-100">
          <n-input-number
            :value="count"
            size="large"
            min="1"
            max="99"
            :on-update:value="updateCount"
          >
            <template #prefix> <span class="me-1">Количество:</span> </template>
            <template #minus-icon>
              <n-icon :component="ArrowDownCircleOutline" />
            </template>
            <template #add-icon>
              <n-icon :component="ArrowUpCircleOutline" />
            </template>
          </n-input-number>
        </div>
        <n-button
          class="to-cart-button w-100 mt-4"
          size="large"
          round
          color="#535353"
          ghost
          @click="addToCart(product, complectations, count)"
        >
          <n-icon size="22" class="me-2"> <CartOutline /> </n-icon>
          ДОБАВИТЬ В КОРЗИНУ
        </n-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  ArrowDownCircleOutline,
  ArrowUpCircleOutline,
  CartOutline,
  PencilOutline
} from '@vicons/ionicons5'
import type {
  ComplectationInterface,
  ProductInterface
} from '~/interfaces/product'
import type { ImageInterface } from '~/interfaces/image'

/// ///
// Props
const props = defineProps<{
  product: ProductInterface
}>()

/// ///
// Components
const ComplectationSelector = defineAsyncComponent(
  () => import('~/components/ui/pages/ComplectationSelector.vue')
)

/// ///
// Variables
const count = ref<number>(1)
const complectations = ref<ComplectationInterface[]>([])
const coverImage = ref<ImageInterface>({})
const { isAdmin } = storeToRefs($auth())
const cartStore = storeCart()

const calculatedPrice = computed(() => {
  return calculateSummary([
    { product: props.product, complectations: complectations.value, count: 1 }
  ])
})

/// ///
// Functions
function setCoverImage(index: number) {
  coverImage.value = props.product?.images![index]
}

function updateCount(value: number) {
  if (value > 0 && value < 99) {
    count.value = value
  } else {
    count.value = 1
  }
}

function addToCart(
  product: ProductInterface,
  complectations: ComplectationInterface[],
  count: number
) {
  cartStore.addToCart(product, complectations, count)

  $notification(
    `'${product.title?.toLocaleUpperCase()}'  ${count}шт, добавлен в корзину`,
    'success'
  )
}

function handleAssignComplectations(evt: ComplectationInterface[]) {
  complectations.value = evt
}

onMounted(() => {
  if (props.product?.images?.length) setCoverImage(0)
})
</script>

<style lang="scss" scoped>
.product-page-images {
  position: relative;
  min-width: 280px;
  max-width: 100vw;
  height: 100%;
  .image-container {
    .image {
      width: 100%;
    }
  }
  .carousel-container {
    width: 100%;
    min-width: 280px;
    height: 200px;
    .carousel-item {
      width: 260px;
      height: 160px;
      cursor: pointer;
      box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
    }
  }
}
.product-page-info {
  min-width: 280px;
  .product-title {
    text-transform: uppercase;
    font-size: 1.2rem;
  }
  .product-price {
    font-weight: 300;
  }
}
</style>

<style lang="scss">
.image {
  img {
    width: 100%;
  }
}
.items-count {
  .n-input {
    height: 40px;
    border-radius: 0px;
  }
}
</style>
