import type { metaInterface } from '~/interfaces/meta'
import { useStoreSettings } from '~/store/settings'

function serializeMeta(item?: Record<string, any>): metaInterface {
  const { settingsByMetaGetter } = storeToRefs(useStoreSettings())
  const result = {
    meta_title: item?.meta_title
      ? `${
          settingsByMetaGetter.value?.app_name ||
          'Необходима настройка параметров домена'
        } - ${item?.meta_title}`
      : settingsByMetaGetter.value?.app_name ||
        'Необходима настройка параметров домена',
    meta_description: String(
      item?.meta_description ||
        settingsByMetaGetter.value?.app_description ||
        ''
    ),
    meta_image: item?.images
      ? item.images[0]?.url || undefined
      : item?.image?.url ||
        settingsByMetaGetter.value?.app_background?.url ||
        undefined,
    meta_keywords: String(
      item?.meta_keywords || settingsByMetaGetter.value?.app_description || ''
    )
  }
  return result
}

export function generateSeo(item: Record<string, any>) {
  const config = useRuntimeConfig()
  const seoItem: metaInterface = serializeMeta(item)
  const seoPrepared = {
    title: seoItem.meta_title,
    ogTitle: seoItem.meta_title,
    description: seoItem.meta_description,
    ogDescription: seoItem.meta_description,
    ogImage: `${config.public.media}${seoItem.meta_image}`
  }
  return seoPrepared
}
