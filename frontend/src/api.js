export const fetchLitteredPoints = async () => {
  const response = await fetch('/api/cameras')
  const payload = await response.json()
  return payload.data
}
