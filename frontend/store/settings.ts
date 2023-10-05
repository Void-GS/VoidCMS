import type { SettingsInterface } from '~/interfaces/settings'

export const useStoreSettings = defineStore('settings', {
  state: () => {
    return {
      settings: ref<SettingsInterface[]>([]),
      host: ''
    }
  },

  getters: {
    settingsByMetaGetter: (state) => {
      return state.settings.find((item) => item.app_url === state.host)
    }
  },

  actions: {
    setHost(host: string) {
      this.host = host
    },

    async getSettings(payload?: SettingsInterface) {
      if (payload && payload.app_url && this.settingsByMetaGetter) {
        return
      }
      const response: SettingsInterface[] = await $fetch('/settings', {
        query: payload
      })
      if (response.length) this.settings = response as SettingsInterface[]
      return response
    },

    async getSettingsById(id: string) {
      const response: SettingsInterface = await $fetch(`/settings/${id}`, {
        method: 'GET'
      })
      const index = this.settings.findIndex((p) => p.id === response.id)
      if (index > -1) {
        this.settings.splice(index, 1, response)
      } else {
        this.settings.push(response)
      }
      return response
    },

    async createSettings(settings: SettingsInterface) {
      const response: SettingsInterface = await $fetch('/settings', {
        method: 'POST',
        body: generateForm(settings)
      })
      this.settings.push(response)
      return response
    },

    async updateSettings(settings: SettingsInterface) {
      const id = settings.id
      delete settings.id
      const response: SettingsInterface = await $fetch(`/settings/${id}`, {
        method: 'PUT',
        body: generateForm(settings)
      })
      const index = this.settings.findIndex((s) => s.id === response.id)
      if (index > -1) {
        this.settings.splice(index, 1, response)
      } else {
        this.settings.push(response)
      }
      return response
    },

    async deleteSettings(settings: SettingsInterface) {
      const response = await $fetch(`/settings/${settings.id}`, {
        method: 'DELETE'
      })
      this.settings = this.settings.filter((s) => s.id !== settings.id)
      return response
    }
  }
})
