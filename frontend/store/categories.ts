import type {
  CategoryInterface,
  CategoryPostitonInterface
} from '~/interfaces/category'

const findCategoryByTagRecursive = (
  category: CategoryInterface,
  searchTag: keyof CategoryInterface,
  searchValue: string | number
): CategoryInterface | null => {
  if (category[searchTag] === searchValue) {
    return category
  }

  if (category.children && category.children.length > 0) {
    for (const child of category.children) {
      const result: CategoryInterface | null = findCategoryByTagRecursive(
        child,
        searchTag,
        searchValue
      )
      if (result) {
        return result
      }
    }
  }

  return null
}

export const useStoreCategories = defineStore('categories', {
  state: () => {
    return {
      categories: ref<CategoryInterface[]>([])
    }
  },

  getters: {
    categoriesGetter: (state) => state.categories,

    categoryByMetaGetter: (state) => (metaUrl: string) => {
      for (const category of state.categories) {
        const result = findCategoryByTagRecursive(category, 'meta_url', metaUrl)
        if (result) {
          return result
        }
      }
      return null
    },

    categoryByIdGetter: (state) => (id: number) => {
      for (const category of state.categories) {
        const result = findCategoryByTagRecursive(category, 'id', id)
        if (result) {
          return result
        }
      }
      return null
    },

    categoryImageRandomGetter: (state) => {
      return state.categories[getRandomInt(state.categories.length)].image?.url
    },

    categoryGetRandomGetter: (state) => {
      const categories = [...state.categories]

      // Ensure there are at least 3 categories in the state
      if (categories.length < 3) {
        return categories
      }

      const randomCategories = []
      const usedIndices = new Set()

      while (randomCategories.length < 3) {
        const randomIndex = getRandomInt(categories.length)

        if (!usedIndices.has(randomIndex)) {
          randomCategories.push(categories[randomIndex])
          usedIndices.add(randomIndex)
        }
      }

      return randomCategories
    }
  },

  actions: {
    async getCategories() {
      const response: CategoryInterface[] = await $fetch('/categories', {
        method: 'GET'
      })
      if (response) {
        this.categories = response as CategoryInterface[]
      }
      return this.categories
    },

    async getCategoryById(id: string) {
      const response: CategoryInterface = await $fetch(`/categories/${id}`, {
        method: 'get'
      })
      const index = this.categories.findIndex((c) => c.id === response.id)
      if (index > -1) {
        this.categories.splice(index, 1, response)
      } else {
        this.categories.push(response)
      }
      return response
    },

    async createCategory(category: CategoryInterface) {
      const response: CategoryInterface = await $fetch('/categories', {
        method: 'post',
        body: generateForm(category)
      })
      this.categories.push(response)
      return response
    },

    async updateCategory(category: CategoryInterface) {
      const id = category.id
      delete category.id
      const response: CategoryInterface = await $fetch(`/categories/${id}`, {
        method: 'put',
        body: generateForm(category)
      })
      const index = this.categories.findIndex((c) => c.id === response.id)
      if (index > -1) {
        this.categories.splice(index, 1, response)
      } else {
        this.categories.push(response)
      }
      return response
    },

    async updateCategoryPosition(categoryPosition: CategoryPostitonInterface) {
      const id = categoryPosition.id
      delete categoryPosition.id
      const response: CategoryInterface = await $fetch(
        `/categories/${id}/position`,
        {
          method: 'post',
          body: generateForm(categoryPosition)
        }
      )
      return response
    },

    async deleteCategory(category: CategoryInterface) {
      const response = await $fetch(`/categories/${category.id}`, {
        method: 'delete'
      })
      this.getCategories()
      return response
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStoreCategories, import.meta.hot))
}
