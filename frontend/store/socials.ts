import type { SocialInterface } from '~/interfaces/social'

export const useStoreSocials = defineStore('socials', {
  state: () => {
    return {
      socials: ref<SocialInterface[]>([])
    }
  },

  getters: {},

  actions: {
    async getSocials(payload?: SocialInterface) {
      const response: SocialInterface[] = await $fetch('/socials', {
        query: payload
      })
      this.socials = response
      return response
    },

    async getSocialById(id: string) {
      const response: SocialInterface = await $fetch(`/socials/${id}`, {
        method: 'GET'
      })
      const index = this.socials.findIndex((p) => p.id === response.id)
      if (index > -1) {
        this.socials.splice(index, 1, response)
      } else {
        this.socials.push(response)
      }
      return response
    },

    async createSocial(social: SocialInterface) {
      const response: SocialInterface = await $fetch('/socials', {
        method: 'POST',
        body: generateForm(social)
      })
      this.socials.push(response)
      return response
    },

    async updateSocial(social: SocialInterface) {
      const id = social.id
      delete social.id
      const response: SocialInterface = await $fetch(`/socials/${id}`, {
        method: 'PUT',
        body: generateForm(social)
      })
      const index = this.socials.findIndex((p) => p.id === response.id)
      if (index > -1) {
        this.socials.splice(index, 1, response)
      } else {
        this.socials.push(response)
      }
      return response
    },

    async deleteSocial(social: SocialInterface) {
      const response = await $fetch(`/socials/${social.id}`, {
        method: 'DELETE'
      })
      this.socials = this.socials.filter((s) => s.id !== social.id)
      return response
    }
  }
})
