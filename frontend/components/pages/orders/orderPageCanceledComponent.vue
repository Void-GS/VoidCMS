<template>
  <div class="order-shipping col-12">
    <n-h3 class="d-flex w-100 align-items-center">
      <n-text type="error">
        <n-icon class="me-2">
          <CloseOutline />
        </n-icon>
        Заказ Отменен
      </n-text>
    </n-h3>
    <OrderComment :info="order.track_info!" />
  </div>
</template>

<script lang="ts" setup>
import { CloseOutline } from '@vicons/ionicons5'
import type { OrderInterface } from '~/interfaces/order'

/// ///
// Components
const OrderComment = defineAsyncComponent(
  () => import('~/components/ui/pages/OrderCommentComponent.vue')
)

/// ///
// Props
defineProps<{
  order: OrderInterface
}>()
</script>
