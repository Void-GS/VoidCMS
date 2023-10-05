import { defineNuxtPlugin } from '#app'
import { ofetch } from 'ofetch'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  globalThis.$fetch = ofetch.create({
    baseURL: config.public.api,
    onRequest({ options }) {
      const { token } = storeToRefs($auth())
      const headers = token.value ? { authorization: token.value } : {}
      options.headers = headers as HeadersInit
    }
  })
})
