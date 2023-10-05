export function handleEdit(id: number, path: string) {
  $router().push(`${path}${id}`)
}
