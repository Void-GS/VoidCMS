<template>
  <div class="order-processing col-12">
    <n-h3 class="d-flex w-100 align-items-center">
      <n-text type="warning">
        <n-icon class="me-2">
          <StorefrontOutline />
        </n-icon>
        Ваш заказ обрабатывается...
      </n-text>
    </n-h3>
    <OrderComment :info="order.track_info!" />
  </div>
</template>

<script lang="ts" setup>
import { StorefrontOutline } from '@vicons/ionicons5'
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
