// Use environment variable for production, fallback to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

export const fetchFields = async () => {
  const res = await fetch(`${API_BASE_URL}/fields/`);
  if (!res.ok) throw new Error("Failed to fetch fields");
  return res.json();
};

export const fetchFieldDetails = async (id) => {
  const res = await fetch(`${API_BASE_URL}/fields/${id}`);
  if (!res.ok) throw new Error("Failed to fetch field details");
  return res.json();
};

export const fetchFieldReadings = async (id) => {
  const res = await fetch(`${API_BASE_URL}/fields/${id}/readings`);
  if (!res.ok) throw new Error("Failed to fetch field readings");
  return res.json();
};

export const predictIrrigation = async (data) => {
  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to predict irrigation");
  return res.json();
};
