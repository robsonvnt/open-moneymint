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
import {AccountService} from "../../account/AccountService";
import {CategoryService} from "../../category/CategoryService";
import {Checkbox} from "@mui/material";

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
    selectedCategoryCode: string;
}

const TransactionTable: React.FC<TransactionTableProps> = ({checkedAccounts, selectedCategoryCode}) => {

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
    }, [checkedAccounts, selectedCategoryCode]);

    // Transactions
    const loadTransactions = () => {
        const account_codes = Array.from(checkedAccounts.keys()).filter(key => checkedAccounts.get(key) === true);
        let categoryList = []
        if (selectedCategoryCode != "")
            categoryList.push(selectedCategoryCode)
        transactionService.getAll(
            currentDate, account_codes, categoryList
        ).then(transactions => {
            setTransactions(transactions);

            const newTransactionTotalsByDate = new Map<string, number>();
            let grouped = groupTransactionsByDate(transactions)
            grouped.forEach((transactions, date) => {
                const total = transactions.reduce((sum, transaction) => sum + transaction.value, 0);
                newTransactionTotalsByDate.set(date, total);
            });
            setTransactionTotalsByDate(newTransactionTotalsByDate);
            setGroupedTransaction(grouped)
        })
    };

    // Month Navigator
    const [currentDate, setCurrentDate] = useState(new Date());

    useEffect(() => {
        loadTransactions();
    }, [currentDate]);


    // Seleção de itens na tabela
    const [selectedTransactions, setSelectedTransactions] = React.useState<Set<string>>(new Set());
    const [transactionTotalsByDate, setTransactionTotalsByDate] = React.useState<Map<string, number>>(new Map<string, number>());
    const [groupedTransaction, setGroupedTransaction] = React.useState<Map<string, AccountTransaction[]>>(new Map<string, AccountTransaction[]>());


    const handleSelectTransaction = (code: string) => {
        const newSelected = new Set(selectedTransactions);
        if (newSelected.has(code)) {
            newSelected.delete(code);
        } else {
            newSelected.add(code);
        }
        setSelectedTransactions(newSelected);
    };

    const selectedRowStyle = {
        backgroundColor: "#f6f6f6" // escolha a cor que preferir
    };

    const groupTransactionsByDate = (transactions: AccountTransaction[]): Map<string, AccountTransaction[]> => {
        const grouped = new Map<string, AccountTransaction[]>();
        transactions.forEach(transaction => {
            const date = formatDateStr(transaction.date);
            const group = grouped.get(date) || [];
            group.push(transaction);
            grouped.set(date, group);
        });
        return grouped;
    };


    return (
        <React.Fragment>
            <Title>Movimentações</Title>
            <MonthNavigator
                currentDate={currentDate}
                setCurrentDate={setCurrentDate}
            />
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell>Selecionar</TableCell>
                        <TableCell>Data</TableCell>
                        <TableCell>Descrição</TableCell>
                        <TableCell>Categoria</TableCell>
                        <TableCell>Conta</TableCell>
                        <TableCell align="right">Valor</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>

                    {Array.from(groupedTransaction.keys()).map(date => {
                        const transactions = groupedTransaction.get(date);
                        if (!transactions) return null;

                        let saldo = 0.0;
                        if (transactionTotalsByDate.get(date))
                            saldo = transactionTotalsByDate.get(date) as number

                        return (
                            <React.Fragment key={date}>
                                {transactions.map(transaction => (
                                    <TableRow key={transaction.code} style={selectedTransactions.has(transaction.code) ? selectedRowStyle : undefined}>
                                        <TableCell padding="checkbox">
                                            <Checkbox
                                                checked={selectedTransactions.has(transaction.code)}
                                                onChange={() => handleSelectTransaction(transaction.code)}
                                            />
                                        </TableCell>
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
                                <TableRow
                                    style={{backgroundColor: '#eaeaea'}}
                                >
                                    <TableCell colSpan={5} align="right"></TableCell>
                                    <TableCell align="right"
                                               style={{
                                                   color: saldo < 0 ? red_color : green_color,
                                               }}
                                    >
                                        <b style={{marginRight: 10, color: '#444'}}>Saldo do dia: </b> {currencyFormatter.format(saldo)}
                                    </TableCell>
                                </TableRow>

                                <TableRow
                                    style={{backgroundColor: '#fff', height: 30}}
                                >
                                    <TableCell colSpan={6} align="right"></TableCell>
                                </TableRow>

                            </React.Fragment>
                        )
                    })}


                </TableBody>
            </Table>
            <Link color="primary" href="#" onClick={preventDefault} sx={{mt: 3}}>
                See more orders
            </Link>
        </React.Fragment>
    )
        ;
}

export default TransactionTable;