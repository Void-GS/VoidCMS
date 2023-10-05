<template>
  <div v-if="categories?.length" class="categories py-5">
    <div class="d-flex flex-wrap justify-content-center align-items-center">
      <div class="last-category">
        <CategoryCard :category="categories[0]" />
      </div>
      <div class="other-categories d-flex flex-column align-items-between">
        <div class="category-container">
          <CategoryCard :category="categories[1]" />
        </div>
        <div class="category-container">
          <CategoryCard :category="categories[2]" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { CategoryInterface } from '~/interfaces/category'

defineProps<{
  categories?: CategoryInterface[]
}>()

/// ///
// Components
const CategoryCard = defineAsyncComponent(
  () => import('~/components/ui/pages/CategoryCardComponent.vue')
)
</script>

<style lang="scss" scoped>
.category-container {
  position: relative;
  height: 100%;
  //   background: #414141;
}

.last-category,
.other-categories {
  width: 600px;
  height: 800px;
  max-width: 90vw;
  //   background: #323232;
}
</style>
