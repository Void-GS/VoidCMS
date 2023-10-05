import type { PageInterface } from '~/interfaces/page'

export const useStorePages = defineStore('pages', {
  state: () => {
    return {
      pages: ref<PageInterface[]>([])
    }
  },

  getters: {
    pageByMetaGetter: (state) => (metaUrl: string) => {
      return state.pages.find((item) => item.meta_url === metaUrl)
    },
    pagesGetter: (state) => {
      return state.pages.filter((p) => p.visible)
    }
  },

  actions: {
    async getPages(payload?: PageInterface) {
      const response: PageInterface | PageInterface[] = await $fetch('/pages', {
        query: payload
      })
      if (payload?.meta_url) {
        this.pages = [response as PageInterface]
      } else {
        this.pages = response as PageInterface[]
      }
      return response
    },

    async getPageById(id: string) {
      const response: PageInterface = await $fetch(`/pages/${id}`, {
        method: 'GET'
      })
      const index = this.pages.findIndex((p) => p.id === response.id)
      if (index > -1) {
        this.pages.splice(index, 1, response)
      } else {
        this.pages.push(response)
      }
      return response
    },

    async createPage(page: PageInterface) {
      const response: PageInterface = await $fetch('/pages', {
        method: 'POST',
        body: generateForm(page)
      })
      this.pages.push(response)
      return response
    },

    async updatePage(page: PageInterface) {
      const id = page.id
      delete page.id
      const response: PageInterface = await $fetch(`/pages/${id}`, {
        method: 'PUT',
        body: generateForm(page)
      })
      const index = this.pages.findIndex((p) => p.id === response.id)
      if (index > -1) {
        this.pages.splice(index, 1, response)
      } else {
        this.pages.push(response)
      }
      return response
    },

    async deletePage(page: PageInterface) {
      const response = await $fetch(`/pages/${page.id}`, {
        method: 'DELETE'
      })
      this.pages = this.pages.filter((r) => r.id !== page.id)
      return response
    }
  }
})
