import type { MenuOption } from 'naive-ui'
import type { CategoryInterface } from '~/interfaces/category'

export function convertCategoriesToMenuOptions(
  categories: CategoryInterface[]
): MenuOption[] {
  return categories.map((category) => {
    const menuOption: MenuOption = {
      label: () =>
        genLinkLabel(`${category.title}`, `/products/${category.meta_url}`),
      key: `/products/${category.meta_url}`
    }

    if (category.children && category.children.length > 0) {
      menuOption.children = convertCategoriesToMenuOptions(category.children)
    }
    return menuOption
  })
}
