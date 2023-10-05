<template>
  <n-card class="page-card new-order-card mt-4" size="huge">
    <n-h2> {{ `Заказ от ${convertDate(String(order.created_at))}` }} </n-h2>
    <n-divider />
    <div class="order-info d-flex flex-wrap">
      <Steps :step="step" class="col-12 col-md-4" />

      <OrderInfo
        :order="order"
        class="col-12 mt-4 ps-0 ps-md-4 mt-md-0 col-md-8"
      />
      <!-- <div class="order-info-section col-12 mt-4 ps-0 ps-md-4 mt-md-0 col-md-8">
        <n-h4> <strong> Информация о заказе: </strong> </n-h4>
        <div v-for="item in orderInfo" :key="item.title" class="order-info-row">
          <strong class="order-info-row-title" v-text="item.title" />:
          <span
            class="order-info-row-description ms-2"
            v-text="item.description"
          />
        </div>
      </div> -->
      <div class="order-info-section col-12 mt-3">
        <n-h4> <strong> Содержание заказа: </strong> </n-h4>
        <n-table :bordered="false" :single-line="false">
          <thead>
            <tr>
              <th>Наменование</th>
              <th>Количество</th>
              <th>Цена за ед.</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in order.items" :key="item.id">
              <td class="text-uppercase">
                <NuxtLink :to="`/product/${item.product.meta_url}`">
                  {{ item.product.title }}
                </NuxtLink>
              </td>
              <td class="text-end">{{ item.count }}</td>
              <td class="text-end">{{ item.product.price }}₽</td>
            </tr>
          </tbody>
        </n-table>
      </div>
    </div>
    <n-divider />
    <n-h4> <strong> Управление заказом: </strong> </n-h4>

    <n-form ref="formRef" :model="order" size="large">
      <n-form-item path="type" label="Статус заказа">
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-select
          v-else
          v-model:value="order.status"
          :options="options"
          placeholder="Изменить статус заказа"
          size="medium"
          value-field="value"
          label-field="title"
          @update:value="() => {}"
        />
      </n-form-item>
      <n-form-item
        path="track_info"
        label="Комментарий менеджера магазина (Например трек номер)"
      >
        <n-skeleton v-if="loading" size="medium" :sharp="false" />
        <n-input
          v-else
          v-model:value="order.track_info"
          type="textarea"
          placeholder="Введите номер"
        />
      </n-form-item>
      <div class="page-actions mt-4 float-end">
        <n-button type="tertiary" @click="handleOrder">
          Обновить заказ
        </n-button>
      </div>
    </n-form>
  </n-card>
</template>

<script lang="ts" setup>
import type { OrderInterface } from '~/interfaces/order'
import { orderStatuses } from '~/consts/order-statuses'

/// ///
// Components
const Steps = defineAsyncComponent(
  () => import('~/components/ui/pages/StepsComponent.vue')
)
const OrderInfo = defineAsyncComponent(
  () => import('~/components/ui/pages/OrderInfoComponent.vue')
)

/// ///
// Props
const props = defineProps<{
  id?: string
}>()

/// ///
// Variables
const options = [
  {
    title: 'Оформление',
    value: 'paperwork'
  },
  {
    title: 'Ожидает Оплаты',
    value: 'payment'
  },
  {
    title: 'Обрабатывается магазином',
    value: 'processing'
  },
  {
    title: 'В доставке',
    value: 'shipping'
  },
  {
    title: 'Отменен',
    value: 'canceled'
  },
  {
    title: 'Завершен',
    value: 'done'
  }
]

const step = computed(() => {
  const step = order?.value.id ? orderStatuses.indexOf(order.value.status!) : 0
  return step + 1
})

const store = storeOrders()
const order = ref<OrderInterface>({})

const loading = ref<boolean>(false)
if (props.id) {
  loading.value = true
}

/// ///
// Functions
async function handleOrder(e: MouseEvent) {
  e.preventDefault()
  const prepared: OrderInterface = {
    id: order.value.id,
    client: order.value.client,
    order_name: order.value.order_name,
    order_phone: order.value.order_phone,
    order_address: order.value.order_address,
    status: order.value.status,
    track_info: order.value.track_info
  }
  try {
    await store.updateOrder(prepared)
    $router().push('/management/orders')
    $notification('Заказ обновлен', 'success')
  } catch {
    $notification('Ошибка обновления', 'error')
  }
}

async function recieveSocial(id: string | undefined) {
  if (id) {
    const response: OrderInterface = { ...(await store.getOrderById(id)) }
    order.value = response
    loading.value = false
  }
}

recieveSocial(props.id)
</script>

<style lang="scss">
.quill-editor-container,
.ql-editor {
  min-height: 220px;
}
</style>
