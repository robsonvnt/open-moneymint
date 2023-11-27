import React, {useEffect, useState} from 'react';
import {Alert, Box, Container, Grid, Snackbar} from "@mui/material";
import Toolbar from "@mui/material/Toolbar";
import Paper from "@mui/material/Paper";
import {Copyright} from "@mui/icons-material";
import TransactionTable from "./TransactionTable";
import Title from "./Title";


interface TransactionViewProps {
    checkedAccounts: Map<string, boolean>;
    selectedCategoryCode: string;
}


const TransactionView: React.FC<TransactionViewProps> =
    ({
         checkedAccounts,
         selectedCategoryCode
     }) => {

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
                <Toolbar/>
                <Container maxWidth="lg" sx={{mt: 4, mb: 4}}>
                    <Grid container spacing={3}>

                        <Grid item xs={12}>
                            <Paper sx={{p: 2, display: 'flex', flexDirection: 'column'}}>
                                <Title>Filtros</Title>
                            </Paper>
                        </Grid>
                        <Grid item xs={12}>
                            <Paper sx={{p: 2, display: 'flex', flexDirection: 'column'}}>
                                <TransactionTable
                                    checkedAccounts={checkedAccounts}
                                    selectedCategoryCode={selectedCategoryCode}
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


