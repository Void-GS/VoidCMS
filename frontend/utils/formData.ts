export function generateForm(obj: { [key: string]: any }) {
  const formdata = new FormData()

  for (const key in obj) {
    if (Array.isArray(obj[key])) {
      if (obj[key].every((item) => item instanceof File)) {
        // If it's an array of files, send them as an array of files
        const files = obj[key] as File[] // Assuming obj[key] is an array of File objects
        for (let i = 0; i < files.length; i++) {
          formdata.append(`${key}[${i}]`, files[i])
        }
      } else if (obj[key].every((item) => typeof item === 'object')) {
        // If it's an array of objects, stringify it and send as a string
        const arrayAsString = JSON.stringify(obj[key])
        formdata.append(key, arrayAsString)
      } else {
        // If it's a regular array, send each item individually
        const items = obj[key] as any[] // Assuming obj[key] is an array
        for (let i = 0; i < items.length; i++) {
          formdata.append(`${key}[${i}]`, items[i])
        }
      }
    } else {
      formdata.append(key, obj[key])
    }
  }

  return formdata
}
