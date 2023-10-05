<template>
  <div id="layout" class="d-flex flex-column flex-grow-1">
    <TheHeader />
    <div id="controller" />
    <div id="content-slot" class="d-flex flex-column">
      <slot />
      <TheFooter />
    </div>
  </div>
</template>

<script lang="ts" setup>
// Components
const TheHeader = defineAsyncComponent(
  () => import('~/components/layout/TheHeader.vue')
)
const TheFooter = defineAsyncComponent(
  () => import('~/components/layout/TheFooter.vue')
)
</script>

<style lang="scss" scoped>
#layout {
  position: relative;
}
#content-slot {
  position: relative;
  max-width: 100vw;
  height: 100%;
  overflow-x: clip;
}
#intersection-controller {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  border: 2px solid red;
}
</style>
