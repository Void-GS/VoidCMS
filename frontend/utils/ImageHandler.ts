export async function handleRemoveImage(
  evt: Record<string, any>
): Promise<void> {
  if (evt.file.url) {
    await $fetch(`/images/${evt.file.id}`, {
      method: 'delete'
    })
  }
}

export function handleImageOrEmpty(item?: Record<string, any>): string {
  const url = useRequestURL()
  const itemImages = item?.images?.length ? item?.images[0]?.url : false
  const img = item?.image?.url || itemImages || null

  const mediaLink = img
    ? `${$config().media}${img}`
    : `${url.protocol}//${url.host}/images/no-image.svg`
  return mediaLink
}
