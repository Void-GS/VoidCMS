<template>
  <div class="navbar-compensation d-flex flex-column flex-grow-1 p-4">
    <n-h1 class="page-name w-100 d-flex align-items-center">
      {{ page?.name }}
      <n-icon
        v-if="isAdmin"
        class="ms-2 icon-button"
        :size="22"
        @click="handleEdit(page?.id!, '/management/pages/edit/')"
      >
        <PencilOutline />
      </n-icon>
    </n-h1>
    <div class="page-content mt-4" v-html="page?.content" />
  </div>
</template>

<script lang="ts" setup>
import { PencilOutline } from '@vicons/ionicons5'

/// ///
// Variables
const pagesStore = storePages()
const metaUrl = String($route().params.meta_url)
const { isAdmin } = storeToRefs($auth())
const page = pagesStore.pageByMetaGetter(metaUrl)

/// ///
// Meta
useSeoMeta(generateSeo(page!))
</script>
