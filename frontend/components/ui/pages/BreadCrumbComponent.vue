<template>
  <div class="bread-crumbs-component">
    <n-breadcrumb class="mt-1">
      <n-breadcrumb-item>
        <NuxtLink
          to="/"
          class="d-flex align-itens-center px-0 user-select-none"
        >
          <n-icon :size="16" :component="HomeOutline" />
          <span class="ms-1" v-if="breadcrumbs.length < 2">
            {{ settings?.app_name || 'Главная' }}
          </span>
        </NuxtLink>
      </n-breadcrumb-item>
      <template v-for="breadcrumb in breadcrumbs" :key="breadcrumb.url">
        <n-breadcrumb-item v-if="breadcrumb.name">
          <NuxtLink
            v-if="breadcrumb.name"
            :to="breadcrumb.url"
            class="d-flex align-itens-center user-select-none"
          >
            <n-icon
              :size="16"
              :component="setIcon(breadcrumb.type)"
              class="me-1"
            />
            <span class="text-capitalize">{{ breadcrumb?.name }} </span>
          </NuxtLink>
        </n-breadcrumb-item>
      </template>
    </n-breadcrumb>
  </div>
</template>

<script lang="ts" setup>
import {
  CubeOutline,
  HomeOutline,
  LayersOutline,
  LibraryOutline
} from '@vicons/ionicons5'
import type { BreadcrumbInterface } from '~/interfaces/breadcrumb'

/// ///
// Props
defineProps<{
  breadcrumbs: BreadcrumbInterface[]
}>()

const settingsStore = storeSettings()
const { settingsByMetaGetter } = storeToRefs(settingsStore)
const settings = settingsByMetaGetter

/// ///
// Functions
function setIcon(type: string) {
  switch (type) {
    case 'category':
      return LibraryOutline
    case 'product':
      return CubeOutline
    case 'products':
      return LayersOutline
    default:
      return HomeOutline
  }
}
</script>

<style lang="scss" scoped>
.bread-crumbs-component {
  max-width: 90vw;
  overflow: hidden;
}
</style>
