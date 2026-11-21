import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

/** Turn an API error into a readable message for the UI. */
export function errorMessage(error, fallback = 'Something went wrong') {
    const detail = error?.response?.data?.detail;
    if (typeof detail === 'string') return detail;
    if (Array.isArray(detail) && detail.length) {
        return detail.map(d => `${(d.loc || []).slice(1).join('.')}: ${d.msg}`).join('\n');
    }
    if (error?.code === 'ERR_NETWORK') return 'Cannot reach the API. Is the backend running on port 8000?';
    return fallback;
}

export default api;
