import type { ClientInterface } from 'interfaces/client'

export const useStoreClients = defineStore('clients', {
  state: () => {
    return {
      clients: ref<ClientInterface[]>([])
    }
  },

  getters: {},

  actions: {
    async getClients() {
      const response: ClientInterface[] = await $fetch('/clients')
      this.clients = response
      return response
    },

    async deleteClient(client: ClientInterface) {
      const response = await $fetch(`/clients/${client.id}`, {
        method: 'DELETE'
      })
      this.clients = this.clients.filter((c) => c.id !== client.id)
      return response
    },

    async changeRole(client: ClientInterface, role: string) {
      const response: ClientInterface = await $fetch(`/clients/${client.id}`, {
        method: 'PATCH',
        body: { role }
      })
      const index = this.clients.findIndex((c) => c.id === response.id)
      if (index > -1) {
        this.clients.splice(index, 1, response)
      } else {
        this.clients.push(response)
      }
      return response
    }
  }
})
