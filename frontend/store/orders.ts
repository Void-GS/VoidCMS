import type { OrderInterface } from '~/interfaces/order'

export const useStoreOrders = defineStore('orders', {
  state: () => {
    return {
      orders: ref<OrderInterface[]>([])
    }
  },

  getters: {
    orderById: (state) => (id: string) => {
      return state.orders.find((item) => String(item.id) === id)
    }
  },

  actions: {
    async createOrder(order: OrderInterface) {
      const response: OrderInterface = await $fetch('/orders', {
        method: 'POST',
        body: order
      })
      this.orders.push(response)
      return response
    },

    async getOrders(all?: boolean) {
      const query = all ? { all: true } : {}
      const response: OrderInterface[] = await $fetch('/orders', {
        query
      })
      this.orders = response
      return response
    },

    async getOrderById(id: string) {
      const response: OrderInterface = await $fetch(`/orders/${id}`, {
        method: 'GET'
      })
      const index = this.orders.findIndex((o) => o.id === response.id)
      if (index > -1) {
        this.orders.splice(index, 1, response)
      } else {
        this.orders.push(response)
      }
      return response
    },

    async updateOrder(order: OrderInterface) {
      const response: OrderInterface = await $fetch(`/orders/${order.id}`, {
        method: 'PUT',
        body: generateForm(order)
      })

      return response
    },

    async deleteOrder(order: OrderInterface) {
      await $fetch(`/orders/${order.id}`, {
        method: 'DELETE'
      })
      this.orders = this.orders.filter((o) => o.id !== order.id)
    }
  }
})
