<template>
  <div class="payment-online w-100">
    <n-h3 class="d-flex w-100 align-items-center">
      <n-icon class="me-2">
        <WalletOutline />
      </n-icon>
      Онлайн оплата:
    </n-h3>
    <n-button type="warning" size="large" class="w-100" @click="handlePayment">
      Оплатить
    </n-button>
    <n-blockquote class="mt-3">
      Оплата ожидается в течении нескольких суток, после чего администратор
      может отклонить ваш заказ.
    </n-blockquote>
  </div>
</template>

<script lang="ts" setup>
import { WalletOutline } from '@vicons/ionicons5'

/// ///
// functions
function handlePayment() {
  console.log('Time to pay bitch')
}
</script>
