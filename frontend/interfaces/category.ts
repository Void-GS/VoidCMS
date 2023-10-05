import type { ImageInterface } from '~/interfaces/image'

export interface CategoryInterface {
  id?: number
  title?: string
  description?: string
  image?: ImageInterface
  meta_title?: string
  meta_url?: string
  meta_description?: string
  meta_keywords?: string
  parent?: number
  children?: CategoryInterface[]
  image_upload?: File
  nested_categories?: CategoryInterface[]
}

export interface CategoryPostitonInterface {
  id?: number
  parent_id?: string
  position: string
}
