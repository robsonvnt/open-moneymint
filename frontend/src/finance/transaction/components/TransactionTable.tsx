import * as React from 'react';
import Link from '@mui/material/Link';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from "./Title";
import {AccountTransaction, NewAccountTransaction} from "../../models";
import {useEffect, useState} from "react";
import {TransactionService} from "../TransactionService";
import MonthNavigator from "./MonthNavigator";
import {currencyFormatter, formatDateStr} from "../../../helpers/BRFormatHelper";
import {AccountService} from "../../account/AccountService";
import {CategoryService} from "../../category/CategoryService";
import {Alert, Checkbox, Snackbar} from "@mui/material";
import AccountTransactionDialogForm from "./AccountTransactionDialogForm";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add";
import Fab from "@mui/material/Fab";

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

const TransactionTable: React.FC<TransactionTableProps> =
    ({
         checkedAccounts,
         selectedCategoryCode
     }) => {

        const transactionService = TransactionService;
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
                    categories.map((category) => {
                        newCategoriesMap.set(category.code, category.name)
                    })
                    setCategoriesMap(newCategoriesMap);
                })
        }, [selectedCategoryCode, checkedAccounts]);

        // Transactions

        const loadTransactions = () => {
            loadTransactionsWithDate(currentDate);
        };

        const loadTransactionsWithDate = (date: Date) => {
            const account_codes = Array.from(checkedAccounts.keys()).filter(key => checkedAccounts.get(key) === true);
            let categoryList = []
            if (selectedCategoryCode != "")
                categoryList.push(selectedCategoryCode)
            transactionService.getAll(
                date, account_codes, categoryList
            ).then(transactions => {
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

        // Seleção de itens na tabela

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
            backgroundColor: "#f5f8ff" // escolha a cor que preferir
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


        // Transactions
        const [selectedTransactions, setSelectedTransactions] = React.useState<Set<string>>(new Set());
        const [notificationOpen, setNotificationOpen] = React.useState(false);
        const [notificationMessage, setNotificationMessage] = useState<string>("");
        const [statusTransactionAction, setStatusTransactionAction] = useState<"success" | "error">("success");
        const [reloadTransactions, setReloadTransactions] = useState(false);

        const addTransaction = () => {
            setDialogOpen(true)
            setReloadTransactions(true)
        };

        const removeTransaction = () => {
            selectedTransactions.forEach((item) => {
                selectedTransactions.forEach((transaction_code) => {
                    transactionService.delete(transaction_code).then(() => {
                        setStatusTransactionAction("success")
                        setNotificationMessage("Transação removida com sucesso!")
                        setNotificationOpen(true);
                    }).catch(() => {
                        setStatusTransactionAction("error")
                        setNotificationMessage("Erro ao remover a Transação!")
                        setNotificationOpen(true);
                    })

                })
            })
            setSelectedTransactions(new Set());
            loadTransactions();
        };

        const handleNotificationClose = (event: React.SyntheticEvent | Event, reason?: string) => {
            setNotificationOpen(false);
        };

        // Transaction dialog form
        const [dialogOpen, setDialogOpen] = useState(false);

        const handleDialogClose = () => {
            setDialogOpen(false);
        };

        const handleSaveTransaction = (newTransaction: NewAccountTransaction) => {
            transactionService.create(newTransaction).then((transaction) => {
                setStatusTransactionAction("success")
                setNotificationMessage("Transação criada com sucesso!")
                setNotificationOpen(true);
                loadTransactions();
            }).catch(() => {
                setNotificationMessage("Erro ao criar a Transação!")
                setStatusTransactionAction("error")
                setNotificationOpen(true);
            })
        };

        const changeCurrentDate = (dt: Date) => {
            setCurrentDate(dt);
            loadTransactionsWithDate(dt);
        }

        return (
            <React.Fragment>
                <Title>Movimentações</Title>
                <MonthNavigator
                    currentDate={currentDate}
                    setCurrentDate={changeCurrentDate}
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
                                        <TableRow key={transaction.code}
                                                  style={selectedTransactions.has(transaction.code) ? selectedRowStyle : undefined}>
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
                                        style={{backgroundColor: '#f0f0f0'}}
                                    >
                                        <TableCell colSpan={5} align="right"></TableCell>
                                        <TableCell align="right"
                                                   style={{
                                                       color: saldo < 0 ? red_color : green_color,
                                                   }}
                                        >
                                            <b style={{marginRight: 10, color: '#444'}}>Saldo do dia: </b>
                                            <b>{currencyFormatter.format(saldo)}</b>
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

                <AccountTransactionDialogForm
                    open={dialogOpen}
                    onClose={handleDialogClose}
                    onSave={handleSaveTransaction}
                />


                <Snackbar open={notificationOpen} autoHideDuration={5000} onClose={handleNotificationClose}>
                    <Alert onClose={handleNotificationClose} severity={statusTransactionAction} sx={{width: '100%'}}>
                        {notificationMessage}
                    </Alert>
                </Snackbar>


                <Fab
                    color="primary"
                    aria-label={selectedTransactions.size > 0 ? "remove" : "add"}
                    style={{
                        margin: '20px 0',
                        position: 'fixed',
                        bottom: '20px',
                        right: '20px'
                    }}
                    onClick={selectedTransactions.size > 0 ? removeTransaction : addTransaction}
                >
                    {selectedTransactions.size > 0 ? <DeleteIcon/> : <AddIcon/>}
                </Fab>

            </React.Fragment>
        )
            ;
    }

export default TransactionTable;