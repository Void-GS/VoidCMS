import { createDiscreteApi } from 'naive-ui'

const { notification, loadingBar } = createDiscreteApi([
  'notification',
  'loadingBar'
])

export function $notification(
  text: string,
  style?: 'default' | 'error' | 'info' | 'success' | 'warning' | undefined,
  duration = 1500
): void {
  notification.create({
    type: style,
    content: text,
    duration,
    keepAliveOnHover: false
  })
}

export const $loading = loadingBar
