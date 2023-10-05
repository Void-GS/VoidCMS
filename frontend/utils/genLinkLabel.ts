import { RouterLink } from 'vue-router'

export function genLinkLabel(label: string, route: string) {
  return h(
    RouterLink,
    {
      to: route
    },
    { default: () => label }
  )
}
