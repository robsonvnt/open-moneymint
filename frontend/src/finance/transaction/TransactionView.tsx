import React, {useEffect} from 'react';
import {Box, Container, Grid, Typography} from "@mui/material";
import Paper from "@mui/material/Paper";
import {Copyright} from "@mui/icons-material";
import TransactionTable from "./components/TransactionTable";
import Title from "./components/Title";
import FinancialSummaryPaper from "./components/FinancialSummaryPaper";


interface TransactionViewProps {
    checkedAccounts: Map<string, boolean>;
    selectedCategoryCode: string;
    reloadAccounts: () => void;
}


const TransactionView: React.FC<TransactionViewProps> =
    ({
         checkedAccounts,
         selectedCategoryCode,
         reloadAccounts
     }) => {

        const [lastMonthBalance, setLastMonthBalance] = React.useState(0);
        const [totalIncome, setTotalIncome] = React.useState(0);
        const [totalExpenses, setTotalExpenses] = React.useState(0);

        useEffect(() => {

        }, []);

        return (
            <Box
                component="main"
                sx={{
                    backgroundColor: (theme) =>
                        theme.palette.mode === 'light'
                            ? theme.palette.grey[100]
                            : theme.palette.grey[900],
                    flexGrow: 1,
                    height: '100vh',
                    overflow: 'auto',
                }}
            >

                <Container maxWidth="lg" sx={{mt: 4, mb: 4}}>
                    <Grid container spacing={3}>

                        <Grid key="total-movements" item xs={12} md={6} lg={6}>
                            <FinancialSummaryPaper
                                previousBalance={lastMonthBalance}
                                totalIncome={totalIncome}
                                totalExpenses={totalExpenses}
                            />
                        </Grid>
                        {/* Recent Deposits */}
                        <Grid item xs={12} md={6} lg={6}>

                        </Grid>

                        <Grid item xs={12}>
                            <Paper sx={{p: 2, display: 'flex', flexDirection: 'column'}}>
                                <TransactionTable
                                    checkedAccounts={checkedAccounts}
                                    selectedCategoryCode={selectedCategoryCode}
                                    reloadAccounts={reloadAccounts}
                                    lastMonthBalance={lastMonthBalance}
                                    setLastMonthBalance={setLastMonthBalance}
                                    setTotalIncome={setTotalIncome}
                                    setTotalExpenses={setTotalExpenses}
                                />
                            </Paper>
                        </Grid>
                    </Grid>
                    <Copyright sx={{pt: 4}}/>
                </Container>
            </Box>
        );
    }

export default TransactionView;


