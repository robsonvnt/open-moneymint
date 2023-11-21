// src/App.tsx
import React, { useState, useEffect } from 'react';
import { Portfolio } from './investments/portfolio/models';
import PortfolioService from './investments/portfolio/PortfolioService';
import { ThemeProvider, createTheme } from '@mui/material';
import { AuthProvider } from './auth/AuthContext';
import Router from './Router';
import axios from 'axios';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4e79a7',
    },
    text: {
      primary: "#444444", // Cor da fonte padrão
    },

  },
  typography: {
    body1: {
      color: '#444444', // Define a cor padrão para o texto
    },
    h1: {
      color: "#444444", // Cor para h1
    },
    h2: {
      color: "red", // Cor para h2
    },
    h3: {
      color: "#444444", // Cor para h3
    },
  }
});

// adicionando token ao cabeçalho
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    config.headers['Content-Type'] = 'application/json';
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});


const App: React.FC = () => {
   return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <Router />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;