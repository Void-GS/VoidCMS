<template>
  <div
    v-if="$route.params.id"
    id="edit-settings"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <SettingsComponent :id="String($route.params.id)" />
  </div>
</template>

<script lang="ts" setup>
/// ///
// Components
const SettingsComponent = defineAsyncComponent(
  () => import('~/components/pages/management/settingsComponent.vue')
)
</script>
