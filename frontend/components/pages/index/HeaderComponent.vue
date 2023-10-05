<template>
  <div
    class="header-layout d-flex flex-column-reverse flex-lg-row justify-content-center full-height align-self-start"
    :class="{ 'to-hidden': isHidden }"
    has-sider
    sider-placement="left"
  >
    <div class="header-main-layout">
      <img
        :src="
          settingsByMetaGetter?.app_background
            ? `${$config.public.media}${settingsByMetaGetter?.app_background?.url}`
            : '/images/default-background.svg'
        "
        class="image-background puff-in-center"
      />
      <!-- <SceneComponent /> -->
    </div>
    <div
      v-if="categories.length"
      class="head-content head-info d-flex align-items-center justify-content-center flex-wrap navbar-compensation-side"
    >
      <div class="info-container slide-in-fwd-left ps-4">
        <n-config-provider :theme="darkTheme">
          <CategoriesMenu :categories="categories" class="ms-md-1" />
        </n-config-provider>
      </div>
    </div>
    <div
      class="head-content info-container-logo user-select-none d-flex flex-column align-items-center justify-content-center mx-auto navbar-compensation-side col-12 col-md-8 col-lg-6 col-xl-5 p-4"
    >
      <div class="info p-5 scale-in-center">
        <div
          class="info-container-image d-flex justify-content-center mb-4 pb-4"
        >
          <n-image class="info-image" :src="logoLink" preview-disabled />
        </div>
        <n-divider></n-divider>
        <div
          class="info-text"
          strong
          v-text="
            settingsByMetaGetter?.app_description ||
            'Необходимо настроить описание в Параметры -> Настройки доменов'
          "
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { darkTheme } from 'naive-ui'
import type { CategoryInterface } from '~/interfaces/category'

defineProps<{
  categories: CategoryInterface[]
  isHidden: boolean
}>()

/// ///
// Components
const CategoriesMenu = defineAsyncComponent(
  () => import('~/components/ui/pages/CategoriesMenuComponent.vue')
)

/// ///
// Variables
const { settingsByMetaGetter } = storeToRefs(storeSettings())
const logoLink = computed(() => {
  return settingsByMetaGetter?.value?.app_logo?.url
    ? `${$config().media}${settingsByMetaGetter.value?.app_logo?.url}`
    : '/images/logo.svg'
})
</script>

<style lang="scss" scoped>
.info {
  width: 100%;
  // background: $background-glass-dark;
  // backdrop-filter: $background-glass-blur;
}

.image-background {
  object-fit: cover;
  height: 100%;
  width: 100%;
}

.header-layout {
  background-color: #232323;
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
  transition: all 1s ease-out;
  overflow: clip;
  .head-content {
    background: transparent;
    z-index: 1;
    min-height: 100vh;
    transition: all 0.9s ease-out;
  }
  &.to-hidden {
    transition: all 1s ease-in;
    height: 0px;
    .head-content {
      transition: all 0.9s ease-in;
      transform: scale(0.5);
      opacity: 0;
    }
  }
}

.head-info {
  position: relative;
  z-index: 2;
  top: 0;
  bottom: 0;
  left: 0;
  min-height: 100vh;
}

.info-container {
  width: 300px;
  max-width: 90vw;
  padding-top: 2rem;
  padding-bottom: 2rem;
  background: $background-glass-dark;
  backdrop-filter: $background-glass-blur;
}

.info-container-logo {
  min-height: 60vh;
  // margin-top: calc($navbar-height + 1.5rem);
}

.info-image {
  width: 100%;
}

.info-text {
  color: white;
  max-width: 560px;
}

.header-main-layout {
  position: absolute;
  width: 100%;
  height: 100%;
  background: #232323;
  z-index: 0;
}
</style>
