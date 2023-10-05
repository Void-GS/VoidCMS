<template>
  <n-form
    ref="orderRef"
    size="large"
    class="w-100"
    :model="order"
    :disabled="!!orderId"
    :rules="rules"
  >
    <n-h3 class="d-flex w-100 align-items-center">
      <n-icon class="me-2">
        <PersonOutline />
      </n-icon>
      Данные клиента
    </n-h3>
    <n-form-item label="Имя и фамилия" path="order_name">
      <n-input
        v-model:value="order.order_name"
        placeholder="Имя и фамилия получателя(необходимо для доставки)"
      />
    </n-form-item>
    <n-form-item label="Номер телефона" path="order_phone">
      <n-input-group>
        <n-input-group-label size="large"> +7 </n-input-group-label>
        <input
          v-model="order.order_phone"
          v-maska
          class="phone-input light"
          type="text"
          data-maska="(###) ###-##-##"
          placeholder="Введите 10 цифр"
        />
      </n-input-group>
    </n-form-item>
    <n-form-item label="Адрес" path="order_address">
      <n-input
        v-model:value="order.order_address"
        type="textarea"
        :autosize="{
          minRows: 3,
          maxRows: 5
        }"
        placeholder="Адрес для доставки включая индекс."
      />
    </n-form-item>
    <n-form-item label="Комментарий" path="order_comment">
      <n-input
        v-model:value="order.order_comment"
        type="textarea"
        :autosize="{
          minRows: 3,
          maxRows: 5
        }"
        placeholder="Коментарий к заказу"
      />
    </n-form-item>
    <n-form-item v-if="!orderId">
      <n-button class="w-100" @click="handleOrder"> Оформить заказ </n-button>
    </n-form-item>
  </n-form>
</template>

<script lang="ts" setup>
import { PersonOutline } from '@vicons/ionicons5'
import type { FormInst, FormRules, FormValidationError } from 'naive-ui'
import type { OrderInterface } from '~/interfaces/order'
import type { CartItemInterface } from '~/interfaces/cart'

/// ///
// Props
const props = defineProps<{
  orderId?: OrderInterface
  items?: CartItemInterface[]
}>()

/// ///
// Variables
const orderRef = ref<FormInst | null>(null)

const { user } = storeToRefs($auth())
const cartStore = storeCart()
const ordersStore = storeOrders()
const order = ref<OrderInterface>({})

/// ///
// Validation Rules
const rules: FormRules = {
  order_name: [
    {
      required: true,
      message: 'ФИО обязательное поле для заполнения',
      trigger: ['blur']
    }
  ],
  order_phone: [
    {
      required: true,
      validator: (rule, value) => {
        const cleanVal = value.replace(/\D/g, '')
        if (!cleanVal) {
          return false
        } else if (!/^\d+$/.test(cleanVal)) {
          return false
        } else if (cleanVal.length < 10) {
          return false
        }
        return true
      },
      message: 'Номер телефона необходим для оформления доставки',
      trigger: ['blur']
    }
  ],
  order_address: [
    {
      required: true,
      message: 'Адрес необходим для оформления доставки',
      trigger: ['blur']
    }
  ]
}

/// ///
// Functions
async function handleOrder() {
  let validation = false
  await orderRef.value?.validate(
    (errors: Array<FormValidationError> | undefined) => {
      if (!errors) {
        validation = true
      }
    }
  )
  if (validation) {
    order.value.items = props.items?.map((i) => {
      return {
        product: { id: i.product.id },
        complectations: i.complectations,
        count: i.count
      }
    })
    try {
      const response = await ordersStore.createOrder(unref(order))
      cartStore.getCart()
      $router().push(`/orders/${response.id}`)
      $notification(`Заказ №${response.id} создан.`, 'success')
    } catch (error) {
      $notification(`Ошибка: Заполните обязательные поля`, 'error')
    }
  }
}

onMounted(() => {
  if (!order.value.order_name && user.value?.name) {
    order.value.order_name = user.value?.name + ' ' + user.value?.last_name
  }
  if (!order.value.order_address) {
    order.value.order_address = user.value?.address
  }
  if (!order.value.order_phone) {
    order.value.order_phone = user.value?.phone
  }
})
</script>
