<template>
  <div
    id="new-social"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <SocialComponent />
  </div>
</template>

<script lang="ts" setup>
const SocialComponent = defineAsyncComponent(
  () => import('~/components/pages/management/socialComponent.vue')
)
</script>
