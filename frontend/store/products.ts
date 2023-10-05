import type { ProductInterface } from '~/interfaces/product'
import type { PaginationInterface } from '~/interfaces/pagination'

import type { getProductsInterface } from '~/interfaces/getProducts'

export const useStoreProducts = defineStore('products', {
  state: () => {
    return {
      products: [] as ProductInterface[],
      pagination: {} as PaginationInterface
    }
  },

  getters: {
    productByIdGetter: (state) => (id: number) => {
      return state.products.find((item) => item.id === id)
    },
    productByMetaGetter: (state) => (metaUrl: string) => {
      return state.products.find((item) => item.meta_url === metaUrl)
    },
    productByCategoryIdGetter: (state) => (categoryId?: string) => {
      return categoryId
        ? state.products.filter((item) => String(item.category) === categoryId)
        : state.products
    }
  },

  actions: {
    async getProducts(payload?: getProductsInterface) {
      const response = await $fetch.raw('/products', {
        query: payload
      })
      const products = response._data as ProductInterface[]
      const pagination = {
        totalPages: parseInt(String(response.headers.get('X-Total-Pages'))),
        page: parseInt(String(response.headers.get('X-Current-Page')))
      }
      if (pagination.totalPages && pagination.page) {
        this.pagination = pagination
      }
      if (payload?.meta_url) {
        const product = products[0]
        const index = this.products.findIndex((p) => p.id === product?.id)
        if (index > -1) {
          this.products.splice(index, 1, product)
        } else {
          this.products.push(product)
        }
      } else {
        this.products = response._data as ProductInterface[]
      }
      return response
    },

    async getProductById(id: string) {
      const response: ProductInterface = await $fetch(`/products/${id}`, {
        method: 'get'
      })
      const index = this.products.findIndex((c) => c.id === response.id)
      if (index > -1) {
        this.products.splice(index, 1, response)
      } else {
        this.products.push(response)
      }
      return response as ProductInterface
    },

    async createProduct(product: ProductInterface) {
      const response: ProductInterface = await $fetch('/products', {
        method: 'post',
        body: generateForm(product)
      })
      this.products.push(response)
      return response
    },

    async updateProduct(product: ProductInterface) {
      const id = product.id
      delete product.id
      const response: ProductInterface = await $fetch(`/products/${id}`, {
        method: 'put',
        body: generateForm(product)
      })
      const index = this.products.findIndex((c) => c.id === response.id)
      if (index > -1) {
        this.products.splice(index, 1, response)
      } else {
        this.products.push(response)
      }
      return response
    },

    async deleteProduct(product: ProductInterface) {
      const response = await $fetch(`/products/${product.id}`, {
        method: 'delete'
      })
      this.products = this.products.filter((r) => r.id !== product.id)
      return response
    }
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useStoreProducts, import.meta.hot))
}
