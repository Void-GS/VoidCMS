<template>
  <n-card
    class="order-container d-flex flex-column align-items-start col-12 col-md-10 col-xl-8 pb-3"
  >
    <n-h1 class="d-flex align-items-center">
      <n-icon class="me-3">
        <ReceiptOutline />
      </n-icon>
      {{
        order?.id
          ? `Заказ от ${convertDate(order?.created_at!)}`
          : 'Оформление заказа'
      }}
    </n-h1>

    <div
      class="order-content d-flex flex-wrap flex-md-nowrap flex-reverse mt-4"
    >
      <div class="order-steps-container pb-3">
        <Steps :step="step" />
      </div>
      <div
        class="order-input w-100 d-flex flex-column align-items-center ps-md-4"
      >
        <OrderInfo
          v-if="order?.id"
          :order="order!"
          class="col-12 mt-4 mt-md-0 ps-0 col-md-12"
        />
        <OrderTable :items="cartItems" class="mt-4" />
        <component
          :is="currentComponent"
          v-if="currentComponent"
          :items="cartItems"
          :order="order"
        />
      </div>
    </div>
  </n-card>
</template>

<script lang="ts" setup>
import { ReceiptOutline } from '@vicons/ionicons5'
import type { OrderInterface } from '~/interfaces/order'
import type { CartItemInterface } from '~/interfaces/cart'

import { orderStatuses } from '~/consts/order-statuses'

/// ///
// Components
const Steps = defineAsyncComponent(
  () => import('~/components/ui/pages/StepsComponent.vue')
)
const OrderInfo = defineAsyncComponent(
  () => import('~/components/ui/pages/OrderInfoComponent.vue')
)
const OrderTable = defineAsyncComponent(
  () => import('~/components/ui/pages/OrderTableComponent.vue')
)
const OrderPaperwork = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageStepPaperworkComponent.vue')
)
const OrderPayment = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPagePaymentComponent.vue')
)
const OrderProcessing = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageProcessingComponent.vue')
)
const OrderShipping = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageShippingComponent.vue')
)
const OrderDone = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageDoneComponent.vue')
)
const OrderCanceled = defineAsyncComponent(
  () => import('~/components/pages/orders/orderPageCanceledComponent.vue')
)

/// ///
// Props
const props = defineProps<{
  order?: OrderInterface
}>()

/// ///
// Variables
const cartStore = storeCart()
const { cart } = storeToRefs(cartStore)

const cartItems = computed<CartItemInterface[]>(() => {
  return props.order?.items || [...cart.value.items]
})

const step = computed(() => {
  const step = props.order?.id ? orderStatuses.indexOf(props.order.status!) : 0
  return step + 1
})

const currentComponent = computed(() => {
  switch (step.value) {
    case 1:
      return OrderPaperwork
    case 2:
      return OrderPayment
    case 3:
      return OrderProcessing
    case 4:
      return OrderShipping
    case 5:
      return OrderDone
    case 6:
      return OrderCanceled
    default:
      return undefined
  }
})

/// ///
// Functions
function convertDate(time: string) {
  const date = new Date(time)
  return date.toLocaleDateString('ru-RU')
}
</script>
