<template>
  <draggable
    :id="idProp || 'root'"
    tag="ul"
    class="drag-area ps-0"
    v-bind="dragOptions"
    :list="items"
    item-key="id"
    @end="handleMoveNested"
  >
    <template #item="{ element }">
      <div :id="element.id" class="drag-item">
        <div class="drag-item-content d-flex col-12 align-items-center ps-4">
          <div class="drag-item-head d-flex align-items-center w-100">
            <n-icon class="me-3" color="#aaaaaa" size="22">
              <MenuOutline />
            </n-icon>
            <n-image
              :src="handleImageOrEmpty(element)"
              class="item-image me-3"
              object-fit="cover"
            />
            <strong>{{ element.title }}</strong>
            <div
              class="drag-item-actions d-flex align-items-center ms-auto me-4"
            >
              <NuxtLink
                v-if="editPath"
                class="me-2"
                :to="`${editPath}${element.id}`"
              >
                <n-button size="small"> Редактировать </n-button>
              </NuxtLink>
              <n-button
                quaternary
                circle
                type="error"
                @click="handleRemove(element.id)"
              >
                <template #icon>
                  <n-icon><TrashOutline /></n-icon>
                </template>
              </n-button>
            </div>
          </div>
        </div>
        <draggableTable
          :id-prop="element.id"
          class="drag-item-inner pt-5 ms-4"
          :edit-path="editPath"
          :items="element.children"
          @delete="handleRemove"
          @move="handleMoveNested"
        />
      </div>
    </template>
  </draggable>
</template>

<script lang="ts" setup>
import { MenuOutline, TrashOutline } from '@vicons/ionicons5'

const draggable = defineAsyncComponent(() => import('vuedraggable'))

/// ///
// Props
defineProps<{
  items: Record<string, any>[]
  editPath?: string
  idProp?: number
}>()

/// ///
// Variables
const dragOptions = {
  group: 'root',
  ghostClass: 'ghost'
}

/// ///
// Emits
const emit = defineEmits(['move', 'delete'])

/// ///
// Functions
function handleMoveNested(evt: Record<string, any>) {
  emit('move', evt)
}

function handleRemove(id: number) {
  emit('delete', id)
}
</script>
