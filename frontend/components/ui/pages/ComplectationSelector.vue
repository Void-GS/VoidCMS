<template>
  <div class="complectations-selector col-12">
    <div
      v-for="(complectationType, index) in Object.keys(complectations)"
      :key="complectationType"
      class="complectation"
      :class="{ 'mb-3': index < Object.keys(complectations).length - 1 }"
    >
      <div class="complectation-selector d-flex align-items-center">
        <span>{{ complectationType }}:</span>
        <n-select
          class="select-unstyled"
          :options="complectations[complectationType]"
          :value="selected[complectationType].value"
          label-field="value"
          :placeholder="`Выберите ${complectationType}`"
          :render-label="renderLabel"
          @update:value="handleUpdateValue"
        />
      </div>
    </div>
    <!-- <n-divider />
    {{ selected }} -->
  </div>
</template>

<script lang="ts" setup>
import type { ComplectationInterface } from '~/interfaces/product'

/// ///
// Props
const props = defineProps<{
  complectationsProp?: ComplectationInterface[]
}>()

/// ///
// Variables
const complectations = ref<Record<string, any>>({
  ...listToComplectations(unref(props.complectationsProp!))
})
const selected = ref<Record<string, any>>({})

/// ///
// Emits
const emit = defineEmits(['update'])

/// ///
// Functions
function renderLabel(option: ComplectationInterface) {
  return h(
    'div',
    { class: 'd-flex col-12 align-items-center justify-content-between' },
    [
      h('strong', option.value),
      h('span', { class: 'me-1' }, `${option.price_change}₽`)
    ]
  )
}

function handleUpdateValue(value: string, option: ComplectationInterface) {
  const type: string = option.type!
  selected.value[type] = option
}

function setDefault() {
  for (const key in complectations.value) {
    selected.value[key] = complectations.value[key][0]
  }
}

watch(
  selected,
  (newValue) => {
    const payload = { ...unref(newValue) }
    for (const key in payload) {
      payload[key] = [payload[key]]
    }
    emit('update', complectationsToList(payload))
  },
  { deep: true }
)

onBeforeMount(() => {
  setDefault()
})
</script>

<style lang="scss" scoped>
.complectation-selector {
  height: 40px;
  padding-left: 14px;
  border: 1px solid #e0e0e6;
  font-size: 15px !important;
}
</style>
