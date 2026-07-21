import { createApp } from 'vue'

import axios from "axios"

import App from './App.vue'

import index from "../router"

import './style.css'
import { useTheme } from './theme'

const { initTheme } = useTheme()
initTheme()

const app = createApp(App)


const api = axios.create({
    baseURL: "https://project-bey-production.up.railway.app/api",
    headers: {
        "Content-Type": "application/json",
    },
})

api.interceptors.request.use(
    async (config) => {
    const token = localStorage.getItem('auth_token');
    if(token){
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
     return Promise.reject(error);
  }
)

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if(error.response?.status === 401) {
      localStorage.removeItem('auth_token');
    }
    return Promise.reject(error);
  }
)


app.use(index)

app.mount('#app')

export default api
