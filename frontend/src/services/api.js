const API_URL = 'http://127.0.0.1:8000/api';

export const fetchFields = async () => {
  const response = await fetch(`${API_URL}/fields`);
  if (!response.ok) throw new Error('Failed to fetch fields');
  return response.json();
};

export const fetchFieldDetails = async (id) => {
  const response = await fetch(`${API_URL}/fields/${id}`);
  if (!response.ok) throw new Error('Failed to fetch field');
  return response.json();
};

export const fetchFieldReadings = async (id) => {
  const response = await fetch(`${API_URL}/fields/${id}/readings`);
  if (!response.ok) throw new Error('Failed to fetch readings');
  return response.json();
};

export const predictIrrigation = async (data) => {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to predict');
  return response.json();
};
