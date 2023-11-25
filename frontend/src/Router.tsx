import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import PrivateRoute from './PrivateRoute';
import LoginForm from './auth/LoginForm';
import PortfolioSelection from './investments/portfolio/PortfolioSelection';
import InvestmentsList from './investments/investments/InvestmentsList';
import SignupForm from './auth/SignupForm';
import FinanceHome from "./finance/FinanceHome";

const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<LoginForm/>}/>
                <Route path="/signup" element={<SignupForm/>}/>

                <Route path="/investments" element={
                    <PrivateRoute>
                        <PortfolioSelection/>
                    </PrivateRoute>
                }/>
                <Route path="/investments/portfolio/:code" element={
                    <PrivateRoute>
                        <InvestmentsList/>
                    </PrivateRoute>
                }/>
                <Route path="/finances" element={
                    <PrivateRoute>
                        <FinanceHome/>
                    </PrivateRoute>
                }/>
            </Routes>
        </BrowserRouter>
    );
};

export default Router;
