export const fetchLitteredPoints = async () => {
  const response = await fetch("/api/cameras");
  const payload = await response.json();
  return payload.data;
};

export const fetchTop5 = async () => {
  const response = await fetch("/api/cameras/top5");
  const payload = await response.json();
  return payload;
};
