import type { CartItemInterface } from '~/interfaces/cart'

export interface OrderInterface {
  id?: number
  status?:
    | 'paperwork'
    | 'payment'
    | 'processing'
    | 'shipping'
    | 'done'
    | 'canceled'
  client?: string
  order_name?: string
  order_phone?: string
  order_address?: string
  order_comment?: string
  track_info?: string
  items?: CartItemInterface[]
  total_price?: number
  created_at?: string
  updated_at?: string
  viewed?: Boolean
}
