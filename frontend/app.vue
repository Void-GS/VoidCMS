<template>
  <Transition name="loader">
    <n-config-provider
      v-if="loaded"
      class="d-flex flex-grow-1"
      preflight-style-enabled
    >
      <NuxtLayout>
        <NuxtPage />
      </NuxtLayout>
    </n-config-provider>
    <Loader v-else />
  </Transition>
</template>

<script lang="ts" setup>
/// ///
// Components
const Loader = defineAsyncComponent(() => import('~/loader.vue'))

/// ///
// Variables
const loaded = ref<boolean>(false)
onMounted(() => {
  loaded.value = true
})
</script>
