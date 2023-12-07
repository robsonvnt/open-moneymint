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

        const balance = previousBalance + (totalIncome - totalExpenses);

        return (
            <>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontSize: 19}}
                    >
                        Saldo anterio
                    </Typography>
                    <Typography component="p" sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{fontSize: 19}}
                    >
                        {currencyFormatter.format(previousBalance)}
                    </Typography>
                </Box>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontSize: 19}}
                    >
                        Total de entradas
                    </Typography>
                    <Typography component="p" sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{color: green_color, fontSize: 19}}
                    >
                        {currencyFormatter.format(totalIncome)}
                    </Typography>
                </Box>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontSize: 19}}
                    >
                        Total de saídas
                    </Typography>
                    <Typography component="p" sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{color: red_color, fontSize: 19}}
                    >
                        {currencyFormatter.format(totalExpenses)}
                    </Typography>
                </Box>
                <Divider/>
                <Box sx={{display: 'flex', justifyContent: 'space-between'}}
                     style={{marginTop: 10}}
                >
                    <Typography color="text.secondary" sx={{flexGrow: 1, textAlign: 'left'}}
                                style={{fontWeight: 'bold', fontSize: 24}}
                    >
                        Saldo atual
                    </Typography>
                    <Typography sx={{flexGrow: 0, textAlign: 'right'}}
                                style={{
                                    color: balance < 0 ? red_color : green_color,
                                    fontWeight: 'bold', fontSize: 24
                                }}
                    >
                        {currencyFormatter.format(balance)}
                    </Typography>
                </Box>
            </>

        )
            ;
    };

export default FinancialSummaryPaper;
