/* eslint-disable camelcase */
import type { ComplectationInterface } from '~/interfaces/product'

export function complectationsToList(
  inputDict: Record<
    string,
    { id: number; value: string; price_change: string }[]
  >
): ComplectationInterface[] {
  const resultList: {
    id: number
    type: string
    value: string
    price_change: string
  }[] = []

  for (const key in inputDict) {
    if (Object.prototype.hasOwnProperty.call(inputDict, key)) {
      const values = inputDict[key]
      for (const item of values) {
        const newObject = {
          id: item.id,
          type: key,
          value: item.value,
          price_change: item.price_change
        }
        resultList.push(newObject)
      }
    }
  }

  return resultList
}

export function listToComplectations(
  inputList: ComplectationInterface[]
): Record<string, ComplectationInterface[]> {
  const resultDict: Record<string, ComplectationInterface[]> = {}

  for (const item of inputList) {
    const { id, type, value, price_change } = item
    if (!resultDict[type!]) {
      resultDict[type!] = []
    }
    resultDict[type!].push({ id, type, value, price_change })
  }

  return resultDict
}
