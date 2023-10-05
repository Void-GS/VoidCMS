<template>
  <div
    class="products-page-heading col-12 d-flex align-items-center justify-content-center py-4 px-5"
  >
    <div class="products-page-category-image scale-out-center">
      <img
        class="category-image"
        :src="genImage(category?.image?.url)"
        :style="{ transform: `translateY(${scrollPosition * -0.5}px)` }"
      />
    </div>
    <div class="d-flex justify-content-center fade-in w-100">
      <div
        class="products-page-category-info d-flex flex-wrap flex-md-nowrap justify-content-center col-md-9 col-xl-5 p-4"
      >
        <img
          v-if="category?.image"
          class="products-page-category-info-image col-12 col-md-4"
          :src="`${$config.public.media}${category?.image?.url}`"
        />
        <div
          class="products-page-category-info-text mt-3 mt-md-0 col-12 col-md col"
          :class="{
            'ps-4 col-8': category?.image,
            'text-center': !category?.image
          }"
        >
          <n-h1
            class="d-flex align-items-center mb-0 text-capitalize"
            :class="{ 'justify-content-center': !category?.image }"
          >
            {{ category?.id ? `${category.title}` : 'Товары' }}
            <n-icon
              v-if="isAdmin && category?.id"
              color="white"
              class="ms-3 icon-button"
              :size="22"
              @click="handleEdit(category?.id!, '/management/products/edit/')"
            >
              <PencilOutline />
            </n-icon>
          </n-h1>
          <span v-if="category?.id">
            {{ category?.description }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { PencilOutline } from '@vicons/ionicons5'
import type { CategoryInterface } from '~/interfaces/category'

/// ///
// Props
defineProps<{
  category?: CategoryInterface
}>()

/// ///
// Variables
const scrollPosition = ref<number>(0)
const { isAdmin } = storeToRefs($auth())

const { settingsByMetaGetter } = storeSettings()

/// ///
// Functions
const handleScroll = () => {
  setTimeout(() => {
    scrollPosition.value = window.scrollY
  }, 0)
}

function genImage(image?: string): string {
  if (image) {
    return `${$config().media}${image}`
  } else {
    const randomImage = storeCategories().categoryImageRandomGetter
    if (randomImage) {
      return `${$config().media}${randomImage}`
    } else {
      const settingsImage = settingsByMetaGetter?.app_background?.url
      if (settingsImage) {
        return `${$config().media}${settingsImage}`
      } else {
        return '/images/default-background.svg'
      }
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scooped>
.products-page-heading {
  background-color: #232323;

  position: relative;
  width: 100%;
  min-height: 320px;
  overflow: clip;
  z-index: 3;
}

.products-page-category-image {
  position: absolute;
  z-index: 0;
  left: -3vw;
  width: 106vw;
  top: -50%;
}

.category-image {
  object-fit: cover;
  height: 100vh;
  width: 100%;
  filter: blur(8px);
}

.products-page-category-info {
  max-width: 90vw;
  background: $background-glass-dark;
  backdrop-filter: $background-glass-blur;
  color: white;
  h1 {
    color: white;
  }
  box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px,
    rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px,
    rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;
}

.products-page-category-info-image {
  height: 100%;
  object-fit: cover;
}
</style>
