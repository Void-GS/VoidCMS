<template>
  <div class="order-products-table col-12 mb-4">
    <n-h3 class="d-flex w-100 align-items-center">
      <n-icon class="me-2">
        <BagHandleOutline />
      </n-icon>
      Товары
    </n-h3>
    <n-table bordered :single-line="false" size="small">
      <thead>
        <tr>
          <th>Наименование</th>
          <th>Количество</th>
          <th>Цена</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td class="order-product">
            <NuxtLink :to="`/product/${item.product.meta_url}`">
              {{ `${item.product.title} (${item.product.price}₽)` }}
              <template v-for="complectation in item.complectations">
                {{
                  `, ${complectation.type}: ${complectation.value} (${complectation.price_change}₽)`
                }}
              </template>
            </NuxtLink>
          </td>
          <td class="order-count text-end">{{ item.count }}</td>
          <td class="text-end text-nowrap">{{ calculateSummary([item]) }} ₽</td>
        </tr>
      </tbody>
    </n-table>
    <div class="order-summary text-end text-nowrap p-2 w-100">
      <strong>Общая стоимость</strong>: {{ calculateSummary(items) }} ₽
    </div>
  </div>
</template>

<script lang="ts" setup>
import { BagHandleOutline } from '@vicons/ionicons5'
import type { CartItemInterface } from '~/interfaces/cart'

/// ///
// Props
defineProps<{
  items: CartItemInterface[]
}>()
</script>

<style lang="scss" scoped>
.order-count {
  width: 84px;
}
.order-summary {
  width: 100%;
}
</style>
