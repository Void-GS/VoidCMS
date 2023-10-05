<template>
  <n-dropdown
    v-if="isAuthenticated"
    class="user-dropdown"
    trigger="click"
    :options="clientMenuOptions"
    @select="selectMenuItem"
  >
    <n-text class="d-flex user-select-none pointer px-3 py-2 btn-collapsing">
      <n-icon size="22"><PersonOutline /></n-icon>
      <span class="d-none d-md-block ms-2">
        {{ user?.name || user?.email }}
      </span>
    </n-text>
  </n-dropdown>
  <n-text
    v-else
    class="d-flex user-select-none pointer px-2 py-2 btn-collapsing"
    @click="showLoginModal = true"
  >
    <n-icon size="22"><PersonOutline /></n-icon>
    <span class="d-none d-md-block ms-2"> Вход </span>
  </n-text>
  <LoginOrRegister v-model:show-modal="showLoginModal" />
</template>

<script lang="ts" setup>
import { PersonOutline } from '@vicons/ionicons5'
import type { ClientInterface } from '~/interfaces/client'
import { clientMenuOptions } from '~/consts/user-menu'

/// ///
// Props
defineProps<{
  isAuthenticated: boolean
  user?: ClientInterface
}>()

/// ///
// Components
const LoginOrRegister = defineAsyncComponent(
  () => import('~/components/ui/user/LoginOrRegisterModal.vue')
)

/// ///
// Variables
const showLoginModal = ref<boolean>(false)

/// ///
// Functions
function selectMenuItem(value: string): void {
  if (value === 'logout') {
    $auth().signOut()
    $router().push('/')
  }
}
</script>
