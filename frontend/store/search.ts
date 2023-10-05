import type { SearchInterface } from '~/interfaces/search'

export const useStoreSearch = defineStore('search', {
  state: () => {
    return {
      search: ref<SearchInterface>()
    }
  },

  actions: {
    async getResults(query: String) {
      if (query.length >= 1) {
        const response: SearchInterface = await $fetch('/search', {
          query: { query }
        })
        this.search = response
      } else this.search = {} as SearchInterface
    },
    clearResults() {
      this.search = undefined
    }
  }
})
