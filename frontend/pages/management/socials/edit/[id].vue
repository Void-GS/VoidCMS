<template>
  <div
    v-if="$route.params.id"
    id="edit-social"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <SocialComponent :id="String($route.params.id)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const SocialComponent = defineAsyncComponent(
  () => import('~/components/pages/management/socialComponent.vue')
)
</script>
