<template>
  <div id="cart">
    <n-popover class="cart p-4" :show-arrow="false" trigger="click">
      <template #trigger>
        <n-badge :value="cart.items.length" color="#434343" :max="9">
          <n-text
            class="d-flex user-select-none pointer px-3 py-2 btn-collapsing"
          >
            <n-icon size="22"> <BagOutline /> </n-icon>
            <span class="d-none d-md-block ms-2"> Корзина </span>
          </n-text>
        </n-badge>

        <!-- <n-button class="btn-collapsing" quaternary round size="large">
          <template #icon>
            <n-text>
              <n-icon>
                <BagOutline />
              </n-icon>
            </n-text>
          </template>
          <n-badge :value="cart.items.length" color="#434343" :max="9">
            <n-text class="d-none d-md-block ms-2">Корзина</n-text>
          </n-badge>
        </n-button> -->
      </template>
      <template #default>
        <template v-if="cart.items.length">
          <div class="cart-content">
            <n-h3 class="d-flex align-items-center my-0 mb-4" strong>
              <n-icon class="me-2" size="24"> <BagOutline /> </n-icon> Товары:
            </n-h3>
            <n-table
              size="small"
              :bordered="false"
              :single-line="true"
              class="user-select-none mb-4"
            >
              <thead>
                <tr>
                  <th>Название:</th>
                  <th>Цена:</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="item in cart.items"
                  :key="item.product.id"
                  class="cart-item"
                >
                  <td class="w-100">
                    <div class="d-flex align-items-center">
                      <n-ellipsis :line-clamp="1">
                        {{ itemTitle(item) }}
                      </n-ellipsis>
                    </div>
                  </td>
                  <td class="cart-item-price">
                    <div class="d-flex align-items-center">
                      <strong class="price me-3">
                        {{ calculateSummary([item]) }} ₽
                      </strong>
                      <n-icon
                        class="icon-trash ms-auto"
                        size="18"
                        color="red"
                        @click="
                          removeFromCart(item.product.id!, item.complectations!)
                        "
                      >
                        <TrashOutline />
                      </n-icon>
                    </div>
                  </td>
                </tr>
              </tbody>
            </n-table>
            <n-h3 class="d-flex align-items-center flex-wrap mb-4 mt-2" strong>
              <div class="cart-summary-heading d-flex align-itemc-center">
                <n-icon class="me-2" size="24"> <WalletOutline /> </n-icon>
                Общая стоимость:
              </div>
              <div class="ms-auto">
                <n-number-animation
                  :from="0.1"
                  :duration="500"
                  :to="calculateSummary(cart.items)"
                  :active="true"
                  :precision="2"
                />
                ₽
              </div>
            </n-h3>
            <n-button
              class="w-100"
              strong
              secondary
              type="success"
              :disabled="!isAuthenticated"
              @click="handleOrder"
            >
              {{
                isAuthenticated
                  ? 'Перейти к оформлению'
                  : 'Войдите чтобы оформить'
              }}
            </n-button>
          </div>
        </template>
        <template v-else>
          <n-empty description="Корзина пуста!">
            <template #extra>
              Добавьте
              <NuxtLink href="/products">
                <n-text underline strong>товары</n-text> </NuxtLink
              >, чтобы оформить заказ
            </template>
          </n-empty>
        </template>
      </template>
    </n-popover>
  </div>
</template>

<script lang="ts" setup>
import { BagOutline, TrashOutline, WalletOutline } from '@vicons/ionicons5'
import type { CartItemInterface } from '~/interfaces/cart'

/// ///
// Variables
const authStore = $auth()
const cartStore = storeCart()
const { cart } = storeToRefs(cartStore)
const { isAuthenticated } = storeToRefs($auth())

/// ///
// Function
function handleOrder() {
  $router().push('/orders/new')
}

function itemTitle(item: CartItemInterface): string {
  let title = ''
  if (item.count > 1) title = title.concat(`${item.count}шт. `)
  if (item.product.title) title = title.concat(`${item.product.title}`)
  if (item.complectations) {
    item.complectations.forEach((c) => (title = title.concat(`, ${c.value}`)))
  }
  return title
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    cartStore.getCart()
  }
})
</script>

<style lang="scss" scoped>
#cart {
  position: relative;
}
.cart-content {
  width: 370px;
  max-width: 76vw;
}
.cart-item {
  position: relative;
  .cart-item-price {
    white-space: nowrap;
    .icon-trash {
      cursor: pointer;
    }
  }
}
</style>
