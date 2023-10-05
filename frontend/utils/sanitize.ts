import sanitizeHtml from 'sanitize-html'

export function sanitizeText(text: string): string {
  const clean = sanitizeHtml(text, {
    allowedTags: [],
    allowedAttributes: {}
  })
  return clean
}
