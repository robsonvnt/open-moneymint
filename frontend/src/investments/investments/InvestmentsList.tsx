import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import {Card, CardActionArea, Grid, Container} from '@mui/material';
import {Investment, createEmptynvestment, getAssetTypeLabel} from './models';
import InvestmentsService from './InvestmentsService';
import {Portfolio, PortfolioConsolidationModel} from '../portfolio/models';
import PortfolioService from '../portfolio/PortfolioService';
import {clearFloatFormatter} from '../../helpers/BRFormatHelper';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';
import EarningsCard from './components/charts/EarningsCard';
import AssetAccumulationChart from './components/charts/AssetAccumulationChart';
import InvestmentDiversificationChart from './components/charts/InvestmentDiversificationChart';
import FormDialogPortfolio from './components/DialogForm';
import InvestmentCard from './components/InvestmentCard';
import MoneyMineAppBar from "../../app/MoneyMineAppBar";


interface InvestmentsListParams {
    [key: string]: string | undefined; // Assinatura de índice
    // ... seus outros campos específicos ...
    code?: string; // por exemplo, se você tiver um parâmetro de rota 'code'
}

const InvestmentsList: React.FC = () => {
    const [consolidatedPortfolio, setConsolidatedPortfolio] = useState<PortfolioConsolidationModel | null>(null);
    const [investments, setInvestments] = useState<Investment[]>([]);

    const [loadingPortfolio, setLoadingPortfolio] = useState<boolean>(true);
    const [loadingInvestments, setLoadingInvestments] = useState<boolean>(true);

    const [error, setError] = useState<string | null>(null);

    const portfolioService = PortfolioService;

    const {code} = useParams<InvestmentsListParams>();

    const investmentsService = InvestmentsService;

    const [dialogOpen, setDialogOpen] = useState<boolean>(false);
    const [activeTab, setActiveTab] = useState<number>(0);
    const [selectedInvestment, setSelectedInvestment] = useState<Investment>(createEmptynvestment());
    const [reloadChart, setReloadChart] = useState(false);


    // Barra lateral
    const [mobileOpen, setMobileOpen] = useState<boolean>(false);
    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };


    const handleFormSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (code) {
            if (selectedInvestment.code && code) {
                investmentsService.updateInvestment(code, selectedInvestment.code, selectedInvestment)
                    .finally(() => {
                        loadInvestments();
                        setDialogOpen(false);
                    }).catch(() => {
                    setError("Erro ao alterar um investimento.");
                })
            } else {
                investmentsService.createInvestment(code, selectedInvestment)
                    .finally(() => {
                        loadInvestments();
                        setDialogOpen(false);
                    }).catch(() => {
                    setError("Erro ao criar um investimento.");
                })
            }

        } else {
            setError("Nenhum portifólio selecionado.");
        }
    };


    const createInvestment = () => {
        if (code) {
            let newInvestment = createEmptynvestment();
            newInvestment.portfolio_code = code;
            setSelectedInvestment(newInvestment)
            setDialogOpen(true);
            setActiveTab(0);
        }
    }

    const deleteInvestment = () => {
        if (selectedInvestment.code && code) {
            investmentsService.deleteInvestment(code, selectedInvestment.code)
                .finally(() => {
                    loadInvestments();
                    setDialogOpen(false);
                }).catch(() => {
                setError("Erro ao deletar um investimento.");
            })
        }
    }

    const loadInvestments = () => {
        if (code) {
            portfolioService.getConsolidatedByCode(code)
                .then(portfolio => {
                    setConsolidatedPortfolio(portfolio);
                    fetchInvestments(portfolio);
                    setLoadingPortfolio(false);
                    setReloadChart(prev => !prev);
                });
        }
    }


    useEffect(() => {
        loadInvestments();
    }, [code]);

    const selectInvestment = (investment: Investment) => {
        setSelectedInvestment(investment)
        setDialogOpen(true);
        setActiveTab(0);
    }

    const fetchInvestments = async (portfolio: Portfolio) => {
        setLoadingInvestments(true);
        try {
            if (portfolio.code) {
                let investments = await investmentsService.filterByPortifolio(portfolio.code);
                if (Array.isArray(investments)) {
                    setInvestments(investments);
                } else {
                    setError("Erro ao recuperar a lista de investimentos.");
                }
            }
        } catch (error) {
            console.error("There was an error fetching the investments!", error);
            setError("Erro ao recuperar o investimento.");
        } finally {
            setLoadingInvestments(false);
        }
    };

    const groupedInvestments = investments.reduce((groups, investment) => {
        const type = investment.asset_type;
        if (!groups[type]) {
            groups[type] = [];
        }
        groups[type].push(investment);
        return groups;
    }, {} as Record<string, typeof investments>);


    if (loadingPortfolio && loadingInvestments) {
        return <div>Carregando...</div>;
    }

    if (error) {
        return <div>Ocorreu um erro: {error}</div>;
    }

    if (!consolidatedPortfolio) {
        return <div>Nenhum detalhe de portfólio encontrado.</div>;
    }

    if (!investments) {
        return <div>Nenhuma Investimento cadastrado.</div>;
    }


    const net_yield = consolidatedPortfolio.current_balance - consolidatedPortfolio.amount_invested;

    return (
        <>
            <MoneyMineAppBar
                handleDrawerToggle={handleDrawerToggle}
            />
            <Container>
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 5
                }}>
                    <h2 style={{color: '#444444'}}>Detalhes do Portfólio: <b>{consolidatedPortfolio.name}</b></h2>
                </div>

                <Grid container
                      spacing={2}
                      direction="row"
                      alignItems="stretch"
                >
                    <Grid item xs={12} sm={6} md={4} lg={4}
                          style={{display: 'flex'}}>
                        <EarningsCard
                            amount={clearFloatFormatter.format(consolidatedPortfolio.amount_invested)}
                            label='Quantia Investida'
                            valueIncreased={true}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={4}
                          style={{display: 'flex'}}>
                        <EarningsCard
                            amount={clearFloatFormatter.format(consolidatedPortfolio.current_balance)}
                            label='Saldo Atual'
                            valueIncreased={true}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4} lg={4}
                          style={{display: 'flex'}}>
                        <EarningsCard
                            amount={clearFloatFormatter.format(net_yield)}
                            label='Rendimento'
                            valueIncreased={net_yield >= 0}
                            percentageChange={net_yield / consolidatedPortfolio.amount_invested * 100}
                        />
                    </Grid>

                </Grid>

                <Grid container
                      spacing={2}
                      direction="row"
                      alignItems="stretch"
                      marginTop={5}
                >
                    <Grid item xs={12} sm={6} md={8} lg={8}
                          style={{display: 'flex'}}>
                        <AssetAccumulationChart
                            portfolio_code={code ? code : ''}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6} md={4} lg={4}
                          style={{display: 'flex'}}>
                        <InvestmentDiversificationChart
                            portfolio_code={code ? code : ''}
                            reloadChart={reloadChart}
                        />
                    </Grid>

                </Grid>

                <div>
                    <h2>Ativos</h2>
                </div>

                <Grid container spacing={2} direction="row" alignItems="stretch">
                    {Object.keys(groupedInvestments).map((type) => (
                        <React.Fragment key={type}>
                            <Grid item xs={12}>
                                <h4>{getAssetTypeLabel(type)}</h4>
                            </Grid>
                            {groupedInvestments[type].map((investment, index) => (
                                <Grid item xs={12} sm={6} md={4} lg={3} key={index} style={{display: 'flex'}}>
                                    <Card sx={{flex: 1}}>
                                        <CardActionArea>
                                            <InvestmentCard
                                                investment={investment}
                                                onClick={selectInvestment}
                                            />
                                        </CardActionArea>
                                    </Card>
                                </Grid>
                            ))}
                        </React.Fragment>
                    ))}
                </Grid>


            </Container>

            <FormDialogPortfolio
                dialogOpen={dialogOpen}
                setDialogOpen={setDialogOpen}
                portfolio={consolidatedPortfolio}
                investment={selectedInvestment}
                setInvestment={setSelectedInvestment}
                handleFormSubmit={handleFormSubmit}
                deleteInvestment={deleteInvestment}
                activeTab={activeTab}
                setActiveTab={setActiveTab}
                reloadInvestments={loadInvestments}
            />

            <Fab
                color="primary"
                aria-label="add"
                onClick={() => createInvestment()}
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
};

export default InvestmentsList;
