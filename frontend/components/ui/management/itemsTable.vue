<template>
  <n-data-table :columns="columns" :data="data" striped>
    <template #empty>
      <n-empty size="large" description="Нет данных">
        <template #extra>
          <nuxt-link v-if="!noEmptyAction" :to="`${route.path}/new`">
            <n-button to="new" size="large"> Добавить </n-button>
          </nuxt-link>
        </template>
      </n-empty>
    </template>
  </n-data-table>
</template>

<script lang="ts" setup>
import type { TableColumns } from 'naive-ui/es/data-table/src/interface'
/// ///
// Props
defineProps<{
  columns: TableColumns<any>
  data: Object[]
  pagination?: Object
  noEmptyAction?: boolean
}>()

/// ///
// Variables
const route = useRoute()

/// ///
// Functions
</script>
