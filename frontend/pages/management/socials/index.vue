<template>
  <div class="socials col-12 px-4 pb-4">
    <div class="sticky-header d-flex align-items-center">
      <n-h1 class="d-flex align-items-center mb-0">
        <n-icon class="me-2"> <ShareSocialOutline /> </n-icon> Социальные сети:
      </n-h1>
      <n-button color="#323232" class="ms-auto" @click="createSocial()">
        <template #icon>
          <n-icon>
            <add-outline />
          </n-icon>
        </template>
        Добавить соц. сеть
      </n-button>
    </div>
    <ItemsTable :columns="socialsColumns()" :data="socials" />
  </div>
</template>

<script lang="ts" setup>
import { AddOutline, ShareSocialOutline } from '@vicons/ionicons5'

/// ///
// Components
const ItemsTable = defineAsyncComponent(
  () => import('~/components/ui/management/itemsTable.vue')
)

/// ///
// Variables
const socialsStore = storeSocials()
const { socials } = storeToRefs(socialsStore)

/// ///
// Functions
function createSocial() {
  $router().push('socials/new')
}

onMounted(async () => {
  await socialsStore.getSocials()
})
</script>
