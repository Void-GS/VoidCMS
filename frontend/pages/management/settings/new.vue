<template>
  <div
    id="new-settings"
    class="d-flex flex-column justify-content-center align-items-center w-100"
  >
    <SettingsComponent />
  </div>
</template>

<script lang="ts" setup>
const SettingsComponent = defineAsyncComponent(
  () => import('~/components/pages/management/settingsComponent.vue')
)
</script>
