<template>
  <div class="order-info-section">
    <n-h4> <strong> Информация по заказу: </strong> </n-h4>
    <div v-for="item in orderInfo" :key="item.title" class="order-info-row">
      <strong class="order-info-row-title" v-text="item.title" />:
      <span class="order-info-row-description ms-2" v-text="item.description" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { OrderInterface } from '~/interfaces/order'

/// ///
// Props
const props = defineProps<{
  order: OrderInterface
}>()

/// ///
// Variables
const orderInfo = computed(() => {
  return [
    { title: 'ФИО Получателя', description: props.order.order_name },
    { title: 'Адрес', description: props.order.order_address },
    { title: 'Номер телефона', description: `+7 ${props.order.order_phone}` },
    {
      title: 'Дата оформления',
      description: convertDate(String(props.order.created_at))
    },
    {
      title: 'Комментарий заказчика',
      description: props.order.order_comment || 'отсутствует'
    },
    { title: 'Общая стоимость', description: `${props.order.total_price}₽` }
  ]
})
</script>
