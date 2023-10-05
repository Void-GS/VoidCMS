import { useStoreCategories } from '~/store/categories'
import { useStoreProducts } from '~/store/products'
import { useStoreCart } from '~/store/cart'
import { useStorePages } from '~/store/pages'
import { useStoreSettings } from '~/store/settings'
import { useStoreSocials } from '~/store/socials'
import { useStoreClients } from '~/store/clients'
import { useStoreOrders } from '~/store/orders'
import { useStoreSearch } from '~/store/search'

export function storeCategories() {
  return useStoreCategories()
}

export function storeProducts() {
  return useStoreProducts()
}

export function storeCart() {
  return useStoreCart()
}

export function storePages() {
  return useStorePages()
}

export function storeSettings() {
  return useStoreSettings()
}

export function storeSocials() {
  return useStoreSocials()
}

export function storeClients() {
  return useStoreClients()
}

export function storeOrders() {
  return useStoreOrders()
}

export function storeSearch() {
  return useStoreSearch()
}
