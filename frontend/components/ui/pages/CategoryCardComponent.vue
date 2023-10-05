<template>
  <div v-if="category" class="d-flex category p-4 user-select-none">
    <div class="category-container d-flex flex-column w-100">
      <div class="category-edit d-flex align-items-start p-3">
        <div
          v-if="isAdmin"
          class="circled-icon d-flex align-items-center justify-content-center"
          @click="handleEdit(category.id!, '/management/categories/edit/')"
        >
          <n-icon size="22" color="white" class="icon-button">
            <PencilOutline />
          </n-icon>
        </div>
      </div>
      <n-image
        :src="handleImageOrEmpty(category)"
        class="background-image in-card"
        preview-disabled
        object-fit="cover"
      />
      <div
        class="category-info d-flex align-items-center p-4 p-md-5 mt-auto w-100"
      >
        <div class="category-info-container">
          <div class="category-info-title">
            <n-h2 class="d-flex align-items-center text-uppercase mb-0">
              <strong>{{ category.title }}</strong>
            </n-h2>
          </div>
          <div
            v-if="category.description"
            class="category-info-description d-md-block mt-1"
          >
            <n-ellipsis expand-trigger="click" line-clamp="3" :tooltip="false">
              {{ category.description }}
            </n-ellipsis>
          </div>
        </div>
        <div class="category-info-arrow mt-2 ms-auto">
          <NuxtLink :to="`/products/${category.meta_url}`">
            <n-icon size="40" color="white" class="icon-forward">
              <ArrowForwardCircleOutline />
            </n-icon>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ArrowForwardCircleOutline, PencilOutline } from '@vicons/ionicons5'
import type { CategoryInterface } from '~/interfaces/category'

/// ///
// Props
defineProps<{
  category?: CategoryInterface
}>()

/// ///
// Variables
const { isAdmin } = storeToRefs($auth())
</script>

<style lang="scss" scoped>
.category {
  position: relative;
  height: 100%;
  width: 100%;
  //   background: #414141;
}

.category-container {
  position: relative;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
}

.category-info {
  width: 100%;
  color: white;
  background: $background-glass-dark;
  backdrop-filter: $background-glass-blur;
  .category-info-title {
    h2 {
      font-size: 1.8rem;
      letter-spacing: 0.2rem;
      color: white;
      @media (max-width: 420px) {
        font-size: 1rem;
        letter-spacing: 0.1rem;
      }
    }
  }
  .n-text {
    color: white;
  }
}

.background-image {
  position: absolute;
  z-index: -1;
  top: 0;
  left: 0;
  object-fit: cover;
  width: 100%;
  height: 100%;
}

.icon-forward {
  cursor: pointer;
  transition: transform 0.15s ease-out;
  &:hover {
    transform: scaleY(0.94) scaleX(0.94);
    transition: transform 0.15s ease-out;
  }
}

.category-edit {
  position: absolute;
  z-index: 1;
  top: 0;
  right: 0;
}
</style>
