<template>
  <div
    id="new-page"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <PageComponent />
  </div>
</template>

<script lang="ts" setup>
const PageComponent = defineAsyncComponent(
  () => import('~/components/pages/management/pageComponent.vue')
)
</script>
