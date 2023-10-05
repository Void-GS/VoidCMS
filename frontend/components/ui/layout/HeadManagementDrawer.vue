<template>
  <div id="management-drawer">
    <n-button
      v-if="isAdmin"
      class="btn-collapsing"
      type="warning"
      secondary
      @click="activateManagementMenu"
    >
      <template #icon>
        <n-icon>
          <ConstructOutline />
        </n-icon>
      </template>
      <span class="d-none d-lg-block ms-2"> Администрирование </span>
    </n-button>
    <n-config-provider v-if="isAdmin" :theme="darkTheme">
      <n-drawer
        v-model:show="isOpen"
        :width="320"
        placement="left"
        :trap-focus="false"
        to="body"
      >
        <n-drawer-content
          body-content-style="padding: 0;"
          class="management-menu"
          :native-scrollbar="false"
        >
          <template #header>
            <div class="drawer-head d-flex align-items-center px-2">
              <n-icon :size="28" class="me-2"> <ConstructOutline /> </n-icon>
              <n-h2 class="my-0">Администрирование</n-h2>
            </div>
          </template>
          <n-menu :options="managementMenuOptions" />
        </n-drawer-content>
      </n-drawer>
    </n-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { darkTheme } from 'naive-ui'
import { ConstructOutline } from '@vicons/ionicons5'
import { managementMenuOptions } from '~/consts/management-menu'

/// ///
// Props
defineProps<{
  isAdmin: boolean
}>()

/// ///
// Variables
const isOpen = ref<boolean>(false)

/// ///
// Functions
function activateManagementMenu(): void {
  isOpen.value = true
}
</script>
