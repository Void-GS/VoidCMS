<template>
  <div class="complectations">
    <n-form-item path="complectations-container" label="Комплектация">
      <n-skeleton v-if="loading" size="medium" :sharp="false" />
      <div v-else class="complectations col">
        <div class="new-complectation d-flex flex-wrap flex-md-nowrap col-12">
          <div class="new-complectation-title col-12 col-md-8">
            <n-skeleton v-if="loading" size="medium" :sharp="false" />
            <n-input
              v-else
              :key="String(Object.keys(complectations))"
              v-model:value="newComplectation"
              placeholder="Название типа комплектации(напр. Цвет, Размер итд)"
            />
          </div>

          <n-button
            tertiary
            type="success"
            class="add-complectation-button col-12 col-md mt-md-0 mt-3 ms-md-3"
            @click="addComplectationType"
          >
            Добавить
          </n-button>
        </div>

        <div class="complectation-options-container mt-3">
          <div v-if="Object.keys(complectations)" class="complectation-options">
            <div
              v-for="complectationType in Object.keys(complectations)"
              :key="complectationType"
              class="complectation-option p-3 mt-3"
            >
              <n-h4 class="d-flex flex-wrap col-12 align-items-center m-0 mb-3">
                <strong class="mb-2 mb-md-0">{{ complectationType }}:</strong>
                <div
                  class="complectation-type-actions d-flex flex-wrap align-items-center ms-auto"
                >
                  <n-button
                    size="small"
                    @click="openParamModal(complectationType)"
                  >
                    Добавить комплект
                  </n-button>
                  <n-button
                    class="ms-md-2 mt-2 mt-md-0"
                    size="small"
                    color="red"
                    @click="removeType(complectationType)"
                  >
                    Удалить
                  </n-button>
                </div>
              </n-h4>
              <div class="complectation-options-table">
                <n-table bordered :single-line="false">
                  <thead>
                    <tr>
                      <th class="col-9">Описание</th>
                      <th class="col-3 text-end">Изменение цены</th>
                    </tr>
                  </thead>
                  <draggable
                    v-model="complectations[complectationType]"
                    tag="tbody"
                    item-key="value"
                    @update="updateComplectations"
                  >
                    <template #item="{ element }">
                      <tr>
                        <td class="cursor-grab">
                          <div class="d-flex align-items-center col">
                            <n-icon class="me-3" color="#aaaaaa" size="20">
                              <MenuOutline />
                            </n-icon>
                            {{ element.value }}
                          </div>
                        </td>
                        <td class="text-end">
                          <div
                            class="d-flex align-items-center justify-content-end col"
                          >
                            {{ element.price_change }}₽
                            <n-icon
                              class="cursor-pointer ms-2"
                              color="red"
                              size="20"
                              @click="removeOption(element, complectationType)"
                            >
                              <TrashOutline />
                            </n-icon>
                          </div>
                        </td>
                      </tr>
                    </template>
                  </draggable>
                </n-table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </n-form-item>
    <n-config-provider :theme="darkTheme">
      <n-modal
        v-model:show="showModal"
        class="col-12 col-md-8 col-lg-8 col-xl-5"
        preset="card"
        :bordered="true"
        :on-after-leave="closeParamModal"
      >
        <template #header>
          <span class="user-select-none">
            Добавление параметра комплектации:
            <strong class="text-decoration-underline">
              {{ newComplectationOption.type }}
            </strong>
          </span>
        </template>
        <div class="new-complectation-option-content">
          <n-form-item
            path="complectation-option"
            label="Описание комплекта"
            size="large"
          >
            <n-input
              v-model:value="newComplectationOption.value"
              placeholder="Введите описание комплекта"
            />
          </n-form-item>
          <n-form-item
            path="complectation-option"
            label="Изменение в зависимости от базовой цены"
            size="large"
          >
            <n-input
              v-model:value="newComplectationOption.price_change"
              placeholder="Изменение основной цены"
            >
              <template #prefix> ₽ </template>
            </n-input>
          </n-form-item>
        </div>
        <template #footer>
          <div class="new-complectation-option-actions d-flex w-100">
            <div class="new-option-actions ms-auto">
              <n-button tertiary type="success" @click="addComplectationOption">
                Добавить параметр
              </n-button>
              <n-button
                tertiary
                class="ms-md-2"
                type="error"
                @click="closeParamModal"
              >
                Отменить
              </n-button>
            </div>
          </div>
        </template>
      </n-modal>
    </n-config-provider>
  </div>
</template>

<script lang="ts" setup>
import { MenuOutline, TrashOutline } from '@vicons/ionicons5'
import { darkTheme } from 'naive-ui'
import type { ComplectationInterface } from '~/interfaces/product'

/// ///
// Props
const props = defineProps<{
  loading?: boolean
  complectationsProp?: ComplectationInterface[]
}>()

/// ///
// Emits
const emit = defineEmits(['update'])

/// ///
// Variables
const draggable = defineAsyncComponent(() => import('vuedraggable'))

const complectations = ref<Record<string, any>>({
  ...listToComplectations(unref(props.complectationsProp || []))
})
const showModal = ref(false)

const newComplectation = ref<string>()
const newComplectationOption = ref<ComplectationInterface>({})

/// ///
// Functions
function addComplectationType() {
  if (newComplectation?.value?.length) {
    complectations.value[newComplectation.value] = []
    newComplectation.value = undefined
  } else {
    $notification('Необходимо ввести название для типа комплектации', 'error')
  }
}

function addComplectationOption() {
  if (
    newComplectationOption.value.value &&
    newComplectationOption.value.price_change
  ) {
    complectations.value[newComplectationOption.value.type!].push(
      newComplectationOption.value
    )
    updateComplectations()
    closeParamModal()
  } else {
    $notification('Ошибка: Все поля должны быть заполнены', 'error')
  }
}

function removeType(complectationType: string) {
  delete complectations.value[complectationType]
  updateComplectations()
}

function removeOption(
  element: ComplectationInterface,
  complectationType: string
) {
  complectations.value[complectationType] = complectations.value[
    complectationType
  ].filter((i: ComplectationInterface) => i.value !== element.value)
  updateComplectations()
}

function updateComplectations() {
  emit('update', complectationsToList(unref(complectations)))
}

function openParamModal(type: string) {
  newComplectationOption.value.type = type
  showModal.value = true
}

function closeParamModal() {
  newComplectationOption.value = {}
  showModal.value = false
}
</script>

<style lang="scss" scoped>
.complectation-option {
  background-color: #fafafc;
  border: 1px solid #efeff5;
}
</style>
