<template>
  <div class="pagination-container d-flex align-items-center">
    <!-- <strong class="me-2">Cтраницы:</strong> -->
    <n-pagination
      :page="pagination.page || 1"
      :page-count="pagination.totalPages || 1"
      :on-update:page="handlePage"
      :page-slot="6"
    />
  </div>
</template>

<script lang="ts" setup>
import type { PaginationInterface } from 'interfaces/pagination'

/// ///
// Props
defineProps<{
  pagination: PaginationInterface
}>()

/// ////
// Emits
const emit = defineEmits(['update:page'])

/// ///
// Functions
function handlePage(number: number) {
  emit('update:page', number)
}
</script>
