// src/App.tsx
import React, {useState, useEffect} from 'react';
import FormDialogPortfolio from './components/Dialog';
import AddIcon from '@mui/icons-material/Add';
import {Box, Button, Fab} from '@mui/material';
import Container from '@mui/material/Container';
import PortfolioList from './components/PortifolioList';
import {BrowserRouter as Router, Route, Routes, useNavigate} from 'react-router-dom';
import {Portfolio} from './models';
import PortfolioService from './PortfolioService';
import MoneyMineAppBar from "../../app/MoneyMineAppBar";


const PortfolioSelection: React.FC = () => {
    const [portfolios, setPortfolios] = useState<Portfolio[]>([]);
    const [selectedPortfolio, setSelectedPortfolio] = useState<Portfolio>({});
    const [dialogOpen, setDialogOpen] = useState<boolean>(false);
    const service = PortfolioService;
    const navigate = useNavigate();

    const selectPortfolio = (portfolio: Portfolio) => {
        // Navegue para a nova rota com o 'code' do portfólio quando um portfólio for selecionado
        navigate(`/investments/portfolio/${portfolio.code}`);
    };

    const toggleDialog = () => {
        setDialogOpen(true);
        setSelectedPortfolio({});
    };

    const portfolioEdit = (portfolio: Portfolio) => {
        setSelectedPortfolio(portfolio);
        setDialogOpen(true);
    };


    useEffect(() => {
        service.getAll()
            .then(portfolios => setPortfolios(portfolios));
    }, []);


    const adicionarOuAtualizarPortfolio = async (portfolio: Portfolio) => {

        try {

            if (selectedPortfolio.code) {
                service.update(selectedPortfolio.code, portfolio);
                portfolio.code = selectedPortfolio.code;
                setPortfolios(portfolios.map(item => (item.code === portfolio.code ? portfolio : item)));
                setSelectedPortfolio({});
            }
            if (!selectedPortfolio.code) {
                service.create(portfolio).then((createdPortfolio) => {
                    setPortfolios([...portfolios, createdPortfolio]);
                    setSelectedPortfolio({});
                });
            }

        } catch (error) {
            console.error("Error: ", error);
        }
    };

    const deletePortifolio = async (portfolio: Portfolio) => {
        if (portfolio.code) {
            service.delete(portfolio.code).catch(() => {
                setPortfolios([...portfolios, portfolio]);
            });
            setPortfolios(portfolios.filter(item => item.code !== portfolio.code));
        }
    }

    // Barra lateral
    const [mobileOpen, setMobileOpen] = useState(false);
    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    return (
        <>
            <MoneyMineAppBar
                handleDrawerToggle={handleDrawerToggle}
            />
            <Container>
                <FormDialogPortfolio
                    openDialog={dialogOpen}
                    setDialogOpen={setDialogOpen}
                    sendPortfolio={adicionarOuAtualizarPortfolio}
                    portfolio={selectedPortfolio}
                />
                <h2
                style={{
                    marginTop: 80
                }}
                >Portifolios</h2>
                <PortfolioList
                    portfolios={portfolios}
                    aoSelecionar={portfolioEdit}
                    deletePortifolio={deletePortifolio}
                    selectPortfolio={selectPortfolio}
                />
            </Container>
            <Fab
                color="primary"
                aria-label="add"
                onClick={toggleDialog}
                style={{
                    margin: '20px 0',
                    position: 'fixed',
                    bottom: '20px',
                    right: '20px'
                }}  // Posiciona o botão no canto inferior direito
            >
                <AddIcon/>
            </Fab>
        </>
    );
}

export default PortfolioSelection;
