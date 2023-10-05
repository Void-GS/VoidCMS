<template>
  <div v-if="MenuOptionsComputed.length" class="menu-categories-container">
    <div class="menu-categories-menu-container">
      <n-menu
        class="menu-categories"
        :icon-size="28"
        :indent="16"
        :options="MenuOptionsComputed"
        default-expand-all
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { MenuOption } from 'naive-ui'
import type { CategoryInterface } from '~/interfaces/category'

const props = defineProps<{
  categories: CategoryInterface[]
}>()

/// ///
// Variables
const MenuOptionsComputed = ref<MenuOption[]>(
  convertCategoriesToMenuOptions([...props.categories])
)
</script>

<style lang="scss">
$item-height: 28px;

.menu-categories-container {
  .menu-categories-title {
    font-size: 20px;
  }
  .menu-categories-menu-container {
    margin-top: -6px;
  }
  .menu-categories {
    .n-menu-item {
      height: $item-height;
      .n-menu-item-content {
        text-transform: uppercase;
        font-weight: 500;
        letter-spacing: 0.5px;
        height: $item-height;
        padding-right: 16px;
      }
    }
  }
}
</style>
