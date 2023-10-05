import type { CategoryInterface } from '~/interfaces/category'
import type { ProductInterface } from '~/interfaces/product'

export interface SearchInterface {
  categories?: CategoryInterface[]
  products?: ProductInterface[]
}
