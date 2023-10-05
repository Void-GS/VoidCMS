import type { ClientInterface } from '~/interfaces/client'
import type {
  ComplectationInterface,
  ProductInterface
} from '~/interfaces/product'

export interface CartItemInterface {
  id?: number
  product: ProductInterface
  complectations?: ComplectationInterface[]
  count: number
}

export interface CartInterface {
  client?: ClientInterface
  items: CartItemInterface[]
}
