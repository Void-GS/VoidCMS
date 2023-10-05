import { restrictedAccess } from '~/consts/restrictedAccess'
import type { ClientInterface } from '~/interfaces/client'
import { useStoreSettings } from '~/store/settings'

export default defineNuxtRouteMiddleware(async (to) => {
  /// ///
  // Website Meta Info
  const nuxtApp = useNuxtApp()
  const settingsStore = await useStoreSettings()

  let host

  if (process.server) {
    host = nuxtApp.ssrContext?.event.node.req.headers.host
  } else {
    host = window.location.host
  }

  settingsStore.setHost(host!)

  try {
    await settingsStore.getSettings({ app_url: host })
  } catch (error) {
    $notification(
      'Необходимо настроить домен:\nАдминистрирование -> Параметры -> Настройки доменов',
      'warning'
    )
  }

  // /// ///
  // // Auth
  const restrictedKey = Object.keys(restrictedAccess).find((key) =>
    to.fullPath.startsWith('/' + key)
  )

  const user: ClientInterface | undefined = await $auth().getSession()

  if (restrictedKey) {
    const requiredRoles = restrictedAccess[restrictedKey].roles
    if (!requiredRoles.includes(String(user?.role))) {
      showError({
        statusCode: 403
      })
    }
  }
})
