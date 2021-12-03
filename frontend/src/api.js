export const fetchLitteredPoints = async () => {
  const response = await fetch('/api/littered-points')
  const payload = await response.json()
  return payload.data
}
