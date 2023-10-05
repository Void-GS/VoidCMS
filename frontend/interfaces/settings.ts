import type { ImageInterface } from '~/interfaces/image'

export interface SettingsInterface {
  id?: number
  app_name?: string
  app_url?: string
  app_description?: string
  app_logo?: ImageInterface
  app_logo_upload?: File
  app_favicon?: ImageInterface
  app_favicon_upload?: File
  app_background?: ImageInterface
  app_background_upload?: File
  mantinance?: boolean
}
