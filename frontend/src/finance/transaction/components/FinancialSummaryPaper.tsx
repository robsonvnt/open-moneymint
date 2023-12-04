import React from 'react';
import {Paper, Typography, Box} from '@mui/material';
import Divider from "@mui/material/Divider";
import {currencyFormatter, formatMonth} from "../../../helpers/BRFormatHelper";

const red_color = '#e15759';
const green_color = '#59a14f';

interface FinancialSummaryPaperProps {
    previousBalance: number;
    totalIncome: number;
    totalExpenses: number;
}


const FinancialSummaryPaper: React.FC<FinancialSummaryPaperProps> =
    ({
         previousBalance,
         totalIncome,
         totalExpenses

     }) => {

    const balance = previousBalance + (totalIncome-totalExpenses);

        return (
            <Paper
                sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    // height: 200,
                }}
            >
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontSize: 18}}
                    >
                        Saldo anterio
                    </Typography>
                    <Typography component="p" sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{fontSize: 18}}
                    >
                        {currencyFormatter.format(previousBalance)}
                    </Typography>
                </Box>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontSize: 18}}
                    >
                        Total de entradas
                    </Typography>
                    <Typography component="p" sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{color: green_color, fontSize: 18}}
                    >
                        {currencyFormatter.format(totalIncome)}
                    </Typography>
                </Box>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontSize: 18}}
                    >
                        Total de saídas
                    </Typography>
                    <Typography component="p" sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{color: red_color, fontSize: 18}}
                    >
                        {currencyFormatter.format(totalExpenses)}
                    </Typography>
                </Box>
                <Divider/>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}
                     style={{marginTop: 10}}
                >
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontWeight: 'bold', fontSize: 20}}
                    >
                        Saldo atual
                    </Typography>
                    <Typography sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{
                                    color: balance < 0 ? red_color : green_color,
                                    fontWeight: 'bold', fontSize: 20}}
                    >
                        {currencyFormatter.format(balance)}
                    </Typography>
                </Box>

            </Paper>
        );
    };

export default FinancialSummaryPaper;
