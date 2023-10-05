import type { CartItemInterface } from '~/interfaces/cart'
import type {
  ComplectationInterface,
  ProductInterface
} from '~/interfaces/product'

export function calculateSummary(items: CartItemInterface[]): number {
  return items.reduce((acc, item) => {
    let complectationPrice = 0

    if (item.complectations?.length) {
      complectationPrice = item.complectations.reduce((acc, item) => {
        acc = acc + Number(Number(item.price_change).toFixed(2))
        return acc
      }, 0)
    }

    const price: number =
      (Number(item.product.price!) + Number(complectationPrice)) * item.count
    acc = Number((acc + price).toFixed(2))
    return acc
  }, 0)
}

export function compareComplectations(
  complectations: Record<string, any>[],
  inCartComplectations: Record<string, any>[]
): boolean {
  if (complectations.length !== inCartComplectations.length) {
    return false
  }

  const equals = complectations.every(
    (item, index) => item.id === inCartComplectations[index].id
  )

  return equals
}

export function setDefaultComplectations(product: ProductInterface) {
  const complectations: ComplectationInterface[] = []

  const complectationsObject = listToComplectations(
    product.complectations || []
  )

  const complectationKeys = Object.keys(complectationsObject)

  if (complectationKeys.length) {
    complectationKeys.forEach((c) => {
      complectations.push(complectationsObject[c][0])
    })
  }
  return complectations
}

export function removeFromCart(
  productId: number,
  complectations: ComplectationInterface[]
) {
  storeCart().removeFromCart(productId, complectations)
}
