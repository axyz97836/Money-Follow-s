// API Client for MoneyFollows

const API_BASE = '/api';

class ApiError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new ApiError(res.status, body.detail || `Error ${res.status}`);
  }

  return res.json();
}

export const api = {
  health: () => request('/health'),

  search: (data) =>
    request('/search', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  chat: (data) =>
    request('/chat', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

export { ApiError };
