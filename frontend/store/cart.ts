import type {
  ComplectationInterface,
  ProductInterface
} from '~/interfaces/product'
import type { CartInterface, CartItemInterface } from '~/interfaces/cart'

export const useStoreCart = defineStore('cart', {
  state: () => {
    return {
      cart: ref<CartInterface>({ items: [] })
    }
  },

  getters: {
    isInCart: (state) => (id: number) => {
      return state.cart.items.findIndex((item) => item.product.id === id) > -1
    }
  },

  actions: {
    async fetchCartItem(item: Record<string, any>): Promise<CartItemInterface> {
      const response: CartItemInterface = await $fetch('/cart', {
        method: 'POST',
        body: item
      })
      return response
    },

    async getCart() {
      const response: CartInterface = await $fetch('/cart')
      this.cart = response
    },

    async addToCart(
      product: ProductInterface,
      complectations: ComplectationInterface[],
      count: number
    ) {
      const payload: Record<string, any> = {
        product_id: product.id,
        complectations,
        count: count || 1
      }
      const cartItemIndex = this.cart.items.findIndex(
        (item) =>
          item.product.id === product.id &&
          compareComplectations(complectations, item.complectations!)
      )
      const isPresent = cartItemIndex > -1
      const isAuthenticated = $auth().isAuthenticated

      if (isAuthenticated) {
        if (isPresent) {
          payload.id = this.cart.items[cartItemIndex].id
          const item = await this.fetchCartItem(payload)
          this.cart.items.splice(cartItemIndex, 1, item)
        } else {
          const item = await this.fetchCartItem(payload)
          this.cart.items.push(item)
        }
      } else {
        const item = { product, complectations, count }
        if (isPresent) {
          this.cart.items.splice(cartItemIndex, 1, item)
        } else {
          this.cart.items.push(item)
        }
      }
    },

    async removeFromCart(
      productId: number,
      complectations?: ComplectationInterface[]
    ) {
      const index = this.cart.items.findIndex((i) =>
        i.product.id === productId && complectations
          ? compareComplectations(complectations, i.complectations!)
          : true
      )

      const itemId = this.cart.items[index].id
      this.cart.items.splice(index, 1)
      if ($auth().isAuthenticated) {
        await $fetch('/cart', {
          method: 'DELETE',
          body: {
            id: itemId
          }
        })
      }
    }
  }
})
