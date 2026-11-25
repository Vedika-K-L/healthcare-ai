import axios from 'axios';
export const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:4000/api',timeout:12000});
api.interceptors.request.use(config=>{const token=localStorage.getItem('hb_token');if(token)config.headers.Authorization=`Bearer ${token}`;return config;});
api.interceptors.response.use(response=>response,error=>{const message=error.response?.data?.message||(!error.response?'Unable to reach HealthBridge. Is the API running?':'Something went wrong. Please try again.');return Promise.reject(new Error(message));});
export const dataOf=<T,>(response:{data:{data:T}})=>response.data.data;
