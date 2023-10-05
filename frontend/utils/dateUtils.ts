export function convertDate(time: string) {
  const date = new Date(time)
  return date.toLocaleDateString('ru-RU')
}
