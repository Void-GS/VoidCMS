<template>
  <n-config-provider :theme="isDark ? darkTheme : lightTheme">
    <div
      id="header"
      class="the-header d-flex justify-content-between align-items-center py-2 px-3 px-md-5"
      :class="{ dark: isDark, pinned: isPinned }"
      item-responsive
    >
      <div class="the-header-logo-container d-flex align-items-center">
        <div class="the-header-logo">
          <nuxt-link to="/">
            <img class="logo-image" alt="" :src="logoLink" />
          </nuxt-link>
        </div>
      </div>
      <div
        class="the-header-search d-flex justify-content-start me-2 me-md-auto me-sm-auto ms-auto ms-sm-4"
      >
        <Search />
      </div>
      <div class="d-flex text-primary align-items-center justify-content-end">
        <HeadManagmementDrawer class="d-none d-md-block" :is-admin="isAdmin" />
        <UserMenu :is-authenticated="isAuthenticated" :user="user" />
        <Cart clas="me-1" />
      </div>
    </div>
  </n-config-provider>
</template>

<script lang="ts" setup>
import { darkTheme, lightTheme } from 'naive-ui'

/// ///
// Components
const HeadManagmementDrawer = defineAsyncComponent(
  () => import('~/components/ui/layout/HeadManagementDrawer.vue')
)
const Search = defineAsyncComponent(
  () => import('~/components/ui/layout/SearchComponent.vue')
)
const UserMenu = defineAsyncComponent(
  () => import('~/components/ui/layout/UserMenu.vue')
)
const Cart = defineAsyncComponent(
  () => import('~/components/ui/layout/CartComponent.vue')
)

/// ///
// Variables
const { user, isAuthenticated } = storeToRefs($auth())
const isPinned = ref<boolean>(false)
const route = useRoute()
const { settingsByMetaGetter } = storeToRefs(storeSettings())

/// ///
// Computed
const logoLink = computed(() => {
  return settingsByMetaGetter?.value?.app_logo?.url
    ? `${$config().media}${settingsByMetaGetter.value?.app_logo?.url}`
    : '/images/logo.svg'
})

const isDark = computed(() => {
  return route.name === 'index'
})

const isAdmin = computed(() => {
  return unref(isAuthenticated.value) && unref(user)?.role === 'admin'
})

/// ///
// Functions
function handleScroll(): void {
  // if (isDark.value) {
  if (window.scrollY > 48) {
    isPinned.value = true
  } else {
    isPinned.value = false
  }
  // }
}

onMounted(() => {
  document.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  document.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss">
.the-header-logo {
  height: 48px;
}

.logo-image {
  object-fit: contain;
  height: 100%;
}

.user-dropdown {
  width: 280px;
}

.the-header {
  overflow-x: clip;
  max-width: 100vw;
  position: fixed;
  height: $navbar-height;
  width: 100%;
  z-index: 8;
  filter: blur(0);
  .logo-image {
    transition: opacity 0.3s ease-out, filter 0.5s ease-out;
    filter: brightness(0);
  }
  transition: color 0.35s ease-in;
  &.pinned {
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 12px;
    background-color: $background-glass-light;
    backdrop-filter: $background-glass-blur;
    transition: color 0.35s ease-out;
  }
}

.dark {
  &.the-header {
    position: absolute;
    .logo-image {
      opacity: 1;
      filter: brightness(1);
      transition: width 0.3s ease-out;
    }
    &.pinned {
      position: fixed;
      animation: slide-in-blurred-top 0.6s cubic-bezier(0.23, 1, 0.32, 1) both;
      background: $background-glass-dark;

      .logo-image {
        opacity: 1;
        width: 100%;
        transition: width 0.3s ease-in;
      }
    }
  }
}

@keyframes slide-in-blurred-top {
  0% {
    transform: translateY(-10px) scaleY(1.2) scaleX(1.2);
    transform-origin: 50% 0%;
    opacity: 0;
  }
  10% {
    opacity: 0;
  }
  100% {
    transform: translateY(0) scaleY(1) scaleX(1);
    transform-origin: 50% 50%;
    opacity: 1;
  }
}
</style>
