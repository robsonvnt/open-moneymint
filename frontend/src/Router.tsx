import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import LoginForm from './auth/LoginForm';
import PortfolioSelection from './investments/portfolio/PortfolioSelection';
import InvestmentsList from './investments/investments/InvestmentsList';
import { AppBar, Toolbar, Typography } from '@mui/material';
import SignupForm from './auth/SignupForm';

const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <AppBar position="static" className='App-header'>
                <Toolbar style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                        <Typography variant="h6" style={{ cursor: 'pointer' }}>
                            Meus Investimentos
                        </Typography>
                    </Link>
                    <Link to="/login" // ou para qualquer rota que você deseja redirecionar após o logout
                        style={{ textDecoration: 'none', color: 'inherit' }}
                        onClick={() => {
                            localStorage.removeItem('accessToken'); // Removendo o token
                        }}
                    >
                        <Typography variant="h6" style={{ cursor: 'pointer' }}>
                            Logout
                        </Typography>
                    </Link>
                </Toolbar>
            </AppBar>
            <Routes>
                <Route path="/login" element={<LoginForm />} />
                <Route path="/signup" element={<SignupForm />} />
                <Route path="/" element={
                    <PrivateRoute>
                        <PortfolioSelection />
                    </PrivateRoute>
                } />
                <Route path="/portfolio/:code" element={
                    <PrivateRoute>
                        <InvestmentsList />
                    </PrivateRoute>
                } />
            </Routes>
        </BrowserRouter>
    );
};

export default Router;
