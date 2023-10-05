export function parseRouteProductsSlugs(slugs: string[]): {
  [key: string]: string
} {
  const route: Record<string, string> = {}

  if (slugs) {
    slugs.forEach((slug) => {
      const parsedNumber = parseInt(slug)

      if (!isNaN(parsedNumber)) {
        route.page = slug
      } else {
        route.category_url = slug
      }
    })
  }

  return route
}
