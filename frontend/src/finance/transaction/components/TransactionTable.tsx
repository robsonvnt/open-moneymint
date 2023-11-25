import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from "./Title";
import {AccountTransaction} from "../../models";
import {useEffect, useState} from "react";
import {TransactionService} from "../TransactionService";
import MonthNavigator from "./MonthNavigator";
import {currencyFormatter, formatDateStr} from "../../../helpers/BRFormatHelper";

// Generate Order Data
function createData(
    id: number,
    date: string,
    name: string,
    shipTo: string,
    paymentMethod: string,
    amount: number,
) {
    return {id, date, name, shipTo, paymentMethod, amount};
}

const red_color = '#e15759';
const green_color = '#59a14f';

function preventDefault(event: React.MouseEvent) {
    event.preventDefault();
}

export default function TransactionTable() {
    const transactionService = TransactionService;
    const [transactions, setTransactions] = React.useState<AccountTransaction[]>([]);


    useEffect(() => {
        loadTransactions();
    }, []);

    // Transactions
    const loadTransactions = () => {
        transactionService.getAll(currentDate).then(transactions => {
            setTransactions(transactions);
        })
    };

    // Month Navigator
    const [currentDate, setCurrentDate] = useState(new Date());

    useEffect(() => {
        loadTransactions();
    }, [currentDate]); // O useEffect será re-executado quando 'currentDate' mudar



    return (
        <React.Fragment>
            <Title>Recent Orders</Title>
            <MonthNavigator
                currentDate={currentDate}
                setCurrentDate={setCurrentDate}
            />
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>Data</TableCell>
                        <TableCell>Descrição</TableCell>
                        <TableCell>Categoria</TableCell>
                        <TableCell>Conta</TableCell>
                        <TableCell align="right">Valor</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {transactions.map((transaction) => (
                        <TableRow key={transaction.code}>
                            <TableCell>
                                {formatDateStr(transaction.date)}
                            </TableCell>
                            <TableCell>{transaction.description}</TableCell>
                            <TableCell>{transaction.category_code}</TableCell>
                            <TableCell>{transaction.account_code}</TableCell>
                            <TableCell
                                align="right"
                                style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    color: transaction.value < 0 ? red_color : green_color
                                }}
                            >
                                {`${currencyFormatter.format(transaction.value)}`}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
            <Link color="primary" href="#" onClick={preventDefault} sx={{mt: 3}}>
                See more orders
            </Link>
        </React.Fragment>
    );
}