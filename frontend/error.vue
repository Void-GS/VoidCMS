<template>
  <div id="error-page">
    <main>
      <div
        id="error"
        class="d-flex justify-content-center align-items-center full-height p-5"
      >
        <n-card class="error-card">
          <template #header>
            <n-h1 class="d-flex align-items-center">
              <n-icon class="me-3" color="red">
                <alert-circle-outline />
              </n-icon>
              Произошла ошибка... {{ error.statusCode }}
            </n-h1>
          </template>
          <n-h3>
            {{ error.message }}
          </n-h3>
          <div class="error-text">
            Вы можете вернуться на главную и выбрать что-то другое, или
            попробовать еще раз.
          </div>
          <template #action>
            <div class="d-flex justify-content-end">
              <n-button class="ms-auto" size="large" @click="handleError">
                Вернуться на главную
              </n-button>
            </div>
          </template>
        </n-card>
      </div>
      <div>
        <svg
          class="waves"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          viewBox="0 24 150 28"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="wave-gradient" gradientTransform="rotate(90)">
              <stop offset="5%" stop-color="#212121" />
              <stop offset="35%" stop-color="#434343" />
            </linearGradient>
            <path
              id="a"
              d="M-160 44c30 0 58-18 88-18s58 18 88 18 58-18 88-18 58 18 88 18v44h-352z"
            />
          </defs>
          <g class="wave-paths">
            <use xlink:href="#a" x="0" />
            <use xlink:href="#a" x="50" y="3" />
            <use xlink:href="#a" x="100" y="5" />
            <use xlink:href="#a" x="150" y="7" />
          </g>
        </svg>
      </div>
    </main>
  </div>
</template>

<script setup>
import { AlertCircleOutline } from '@vicons/ionicons5'

defineProps({
  error: Object
})

// Create Custom Errors
const errorConst = useError()

if (errorConst.value.statusCode === 404) {
  errorConst.value.message =
    'Увы, но страница которую вы ищете, в данный момент недоступна. Очень сожалеем Т_т'
}

if (errorConst.value.statusCode === 403) {
  errorConst.value.message =
    'К сожалению для доступа к этой странице у вас не хватает прав.'
}

const handleError = () => clearError({ redirect: '/' })

/// ///
// Meta
useSeoMeta(generateSeo({}))
</script>

<style lang="scss" scoped>
.error-card {
  max-width: 640px;
  min-width: 320px;
}

main {
  height: 100vh;
  width: 100vw;
  position: relative;
  //   background: linear-gradient(to right, #b92b27, #1565c0);
  overflow-x: hidden;
}

.waves {
  position: fixed;
  top: 65%;
  left: 0;
  width: 100%;
  min-width: 1920px;
  height: 50vh;
  z-index: -1;
}

/* Animation */
.wave-paths {
  use {
    animation: move-waves 10s ease-in-out infinite;
    fill: url(#wave-gradient);
  }
  use:nth-child(odd) {
    animation-direction: reverse;
    animation-duration: 13s;
  }
  use:nth-child(1) {
    animation-delay: -2s;
    opacity: 0.7;
  }
  use:nth-child(2) {
    animation-delay: -3s;
    opacity: 0.5;
  }
  use:nth-child(3) {
    animation-delay: -4s;
    opacity: 0.3;
  }
  use:nth-child(4) {
    animation-delay: -5s;
  }
}

@keyframes move-waves {
  0% {
    transform: translate3d(-30px, 0, 0);
  }
  50% {
    transform: translate3d(30px, 0, 0);
  }
  100% {
    transform: translate3d(-30px, 0, 0);
  }
}
</style>
