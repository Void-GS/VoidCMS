<template>
  <n-steps
    class="order-steps user-select-none"
    :current="step"
    :status="'process'"
    vertical
  >
    <!-- <template #finish-icon>
      <n-icon>
        <md-happy />
      </n-icon>
    </template>
    <template #error-icon>
      <n-icon>
        <md-sad />
      </n-icon>
    </template> -->
    <n-step title="Оформление" description="Подтверждаем данные">
      <template #icon>
        <n-icon>
          <ReorderFourOutline />
        </n-icon>
      </template>
    </n-step>
    <n-step title="Оплата" description="Оплата выбранных товаров">
      <template #icon>
        <n-icon>
          <WalletOutline />
        </n-icon>
      </template>
    </n-step>
    <n-step title="Обработка" description="Обрабатка заказа магазином">
      <template #icon>
        <n-icon>
          <StorefrontOutline />
        </n-icon>
      </template>
    </n-step>
    <n-step title="Доставка" description="Высылаем данные о доставке">
      <template #icon>
        <n-icon>
          <TrainOutline />
        </n-icon>
      </template>
    </n-step>
    <n-step title="Завершение" description="Получение и закрытие заказа.">
      <template #icon>
        <n-icon>
          <CheckmarkDoneOutline />
        </n-icon>
      </template>
    </n-step>
  </n-steps>
</template>

<script lang="ts" setup>
import {
  CheckmarkDoneOutline,
  ReorderFourOutline,
  StorefrontOutline,
  TrainOutline,
  WalletOutline
} from '@vicons/ionicons5'

/// ///
// Props
defineProps<{
  step: number
}>()
</script>
