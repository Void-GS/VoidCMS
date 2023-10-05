import type { ImageInterface } from '~/interfaces/image'

export interface ComplectationInterface {
  id?: number
  type?: string
  value?: string
  price_change?: string
}

export interface ProductInterface {
  id?: number
  title?: string
  content?: string
  price?: string | number
  category?: number
  images?: ImageInterface[]
  images_upload?: File[]
  complectations?: ComplectationInterface[]
  visible?: boolean
  is_promotioned?: boolean
  meta_title?: string
  meta_url?: string
  meta_description?: string
  meta_keywords?: string
}
