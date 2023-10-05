<template>
  <div
    id="management"
    class="navbar-compensation d-flex flex-column flex-grow-1"
  >
    <div class="nested-routes justify-content-center d-flex flex-grow-1 px-4">
      <NuxtPage />
    </div>
  </div>
</template>

<style lang="scss" scoped>
#management {
  position: relative;
}
#management-panel {
  position: sticky;
  top: $navbar-height; /* Adjust the top value as needed to set the sticky position */
  background-color: #fff; /* You may adjust the background color as needed */
  z-index: 1;
  &::before {
    position: absolute;
    bottom: 0;
    content: '';
    width: 100%;
    height: 300px;
    background-color: white;
  }
}
</style>
