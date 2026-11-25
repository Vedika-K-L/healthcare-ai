import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { HealthToastProvider } from './components/HealthToast';
import App from './App';
import './i18n';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><BrowserRouter><ThemeProvider><AuthProvider><HealthToastProvider><App/></HealthToastProvider></AuthProvider></ThemeProvider></BrowserRouter></React.StrictMode>);
