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
import TransactionView from "./TransactionView";
import {AccountService} from "../../account/AccountService";
import {CategoryService} from "../../category/CategoryService";

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

interface TransactionTableProps {
    checkedAccounts: Map<string, boolean>;
}

const TransactionTable: React.FC<TransactionTableProps> = ({checkedAccounts}) => {

    const transactionService = TransactionService;
    const [transactions, setTransactions] = React.useState<AccountTransaction[]>([]);
    const [accountsMap, setAccountsMap] = React.useState<Map<string, string>>(new Map());
    const [categoriesMap, setCategoriesMap] = React.useState<Map<string, string>>(new Map());


    useEffect(() => {
        loadTransactions();

        // Carrega todas as Contas
        AccountService.getAllAccounts().then(
            accounts => {
                const newAccountsMap = new Map(accountsMap.entries());
                accounts.map(account => newAccountsMap.set(account.code, account.name))
                setAccountsMap(newAccountsMap)
            })

        // Carrega todas as Categorias
        CategoryService.getAllCategoriesList().then(
            categories => {
                const newCategoriesMap = new Map();
                categories.map(category => {
                    newCategoriesMap.set(category.code, category.name)
                })
                setCategoriesMap(newCategoriesMap)

            })
    }, []);

    useEffect(() => {
        loadTransactions();
    }, [checkedAccounts]);

    // Transactions
    const loadTransactions = () => {
        const account_codes = Array.from(checkedAccounts.keys()).filter(key => checkedAccounts.get(key) === true);
        transactionService.getAll(currentDate, account_codes).then(transactions => {
            setTransactions(transactions);
        })
    };

    // Month Navigator
    const [currentDate, setCurrentDate] = useState(new Date());

    useEffect(() => {
        loadTransactions();
    }, [currentDate]);


    return (
        <React.Fragment>
            <Title>Jaque</Title>
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
                            <TableCell>{categoriesMap.get(transaction.category_code)}</TableCell>
                            <TableCell>{accountsMap.get(transaction.account_code)}</TableCell>
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

export default TransactionTable;