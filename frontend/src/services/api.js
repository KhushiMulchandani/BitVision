import axios from 'axios';

// Base API instance matching your Django server URL
const API = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT Access Token dynamically
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const getSentiment = async () => {
  const response = await API.get('sentiment/');
  return response.data;
};

export default API;