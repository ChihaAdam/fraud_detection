/** Derive a sibling API route from the prediction endpoint set in the footer. */
export function apiEndpoint(endpoint: string, route: string): string {
  const base = endpoint.trim().replace(/\/+$/, '')
  if (base.endsWith('/predict')) {
    return `${base.slice(0, -'/predict'.length)}/${route}`
  }
  return `${base}/${route}`
}
