<template>
  <div
    v-if="$route.params.id"
    id="edit-page"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <PageComponent :id="String($route.params.id)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const PageComponent = defineAsyncComponent(
  () => import('~/components/pages/management/pageComponent.vue')
)
</script>
