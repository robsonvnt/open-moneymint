import * as React from 'react';
import {useEffect, useState} from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from "./Title";
import {AccountConsolidationModel, AccountTransaction, InputAccountTransaction} from "../../models";
import {TransactionService} from "../TransactionService";
import MonthNavigator from "./MonthNavigator";
import {currencyFormatter, formatDateStr} from "../../../helpers/BRFormatHelper";
import {AccountService} from "../../account/AccountService";
import {CategoryService} from "../../category/CategoryService";
import {Alert, Checkbox, DialogContentText, IconButton, Snackbar} from "@mui/material";
import AccountTransactionDialogForm from "./AccountTransactionDialogForm";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add";
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Fab from "@mui/material/Fab";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import {AccountConsolidationsService} from "../../accountConsolidations/AccountConsolidationsService";
import UploadDialog from './UploadDialog';


const red_color = '#e15759';
const green_color = '#59a14f';

interface TransactionTableProps {
    checkedAccounts: Map<string, boolean>;
    selectedCategoryCode: string;
    reloadAccounts: () => void;
    lastMonthBalance: number;
    setLastMonthBalance: React.Dispatch<React.SetStateAction<number>>;
    setTotalIncome: React.Dispatch<React.SetStateAction<number>>;
    setTotalExpenses: React.Dispatch<React.SetStateAction<number>>;
    currentDate: Date;
    setCurrentDate: React.Dispatch<React.SetStateAction<Date>>;
}

const TransactionTable: React.FC<TransactionTableProps> =
    ({
         checkedAccounts,
         selectedCategoryCode,
         reloadAccounts,
         lastMonthBalance,
         setLastMonthBalance,
         setTotalIncome,
         setTotalExpenses,
         currentDate,
         setCurrentDate
     }) => {

        const transactionService = TransactionService;
        const [accountsMap, setAccountsMap] = React.useState<Map<string, string>>(new Map());
        const [categoriesMap, setCategoriesMap] = React.useState<Map<string, string>>(new Map());

        useEffect(() => {


            // Carrega todas as Contas
            AccountService.getAllAccounts().then(
                accounts => {
                    const newAccountsMap = new Map(accountsMap.entries());
                    accounts.map(account => {
                        newAccountsMap.set(account.code, account.name)
                    })
                    setAccountsMap(newAccountsMap)
                    loadTransactions();
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
            // Pega o saldo do mês anterior
            const newDate = new Date(date);
            newDate.setMonth(newDate.getMonth() - 1);
            AccountConsolidationsService.getConsolidation(account_codes, newDate).then((consolidations) => {
                // Calcula salto das contas selecionadas do mês anterior
                let lastMonthBalance = 0;
                consolidations.map(consolidation => lastMonthBalance += consolidation.balance)
                setLastMonthBalance(lastMonthBalance)


                // Cria uma lista com as categorias selecionadas
                let categoryList = []
                if (selectedCategoryCode != "")
                    categoryList.push(selectedCategoryCode)

                transactionService.getAll(
                    date, account_codes, categoryList
                ).then(transactions => {
                    // Monta a  lista de transações agrupadas por dia
                    const newTransactionTotalsByDate = new Map<string, number>();
                    let grouped = groupTransactionsByDate(transactions)

                    let cumulativeBalance = lastMonthBalance;


                    let totalIncome = 0;
                    let totalExpenses = 0;
                    grouped.forEach((transactions, date) => {

                        const dailyTotal = transactions.reduce((sum, transaction) => sum + transaction.value, 0);

                        transactions.map(transaction => {
                            if (transaction.value > 0)
                                totalIncome += transaction.value
                            else
                                totalExpenses -= transaction.value
                        })

                        cumulativeBalance += dailyTotal;
                        newTransactionTotalsByDate.set(date, cumulativeBalance);
                    });
                    setTotalIncome(totalIncome)
                    setTotalExpenses(totalExpenses)

                    setTransactionTotalsByDate(newTransactionTotalsByDate);
                    setGroupedTransaction(grouped)
                })

            })
        };

        // Upload de arquivo TXT de transações
        const [dialogUploadOpen, setDialogUploadOpen] = useState(false);

        const handleOpenDialog = () => {
            setDialogUploadOpen(true);
        };

        const handleCloseDialog = () => {
            setDialogUploadOpen(false);
        };


        // Seleção de itens na tabela

        const [transactionTotalsByDate, setTransactionTotalsByDate] = React.useState<Map<string, number>>(new Map<string, number>());
        const [groupedTransaction, setGroupedTransaction] = React.useState<Map<string, AccountTransaction[]>>(new Map<string, AccountTransaction[]>());
        const [lastMonthConsolidation, setLastMonthConsolidation] = React.useState<AccountConsolidationModel>({balance: 0});


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

        const removeTransaction = async () => {
            for (const transaction_code of Array.from(selectedTransactions)) {
                await deleteTransaction(transaction_code);
            }
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

        const handleSaveTransaction = (transaction: InputAccountTransaction) => {
            if (transaction.code) {
                updateTransaction(transaction)
            } else {
                createTransaction(transaction)
            }
            setTimeout(loadTransactions, 200);
            reloadAccounts()
        };

        const changeCurrentDate = (dt: Date) => {
            setCurrentDate(dt);
            loadTransactionsWithDate(dt);
        }

        const handleEditTransaction = (code: string) => {
            handleCloseMenuTraActions();
            transactionService.get(code).then((loadedTransaction) => {
                setCurrentTransaction(loadedTransaction)
                setDialogOpen(true)
            })
        }
        const handleAddTransaction = () => {
            setCurrentTransaction({})
            setDialogOpen(true)
        };

        // CRUD Transaction
        const [currentTransaction, setCurrentTransaction] = useState<InputAccountTransaction>({});
        const [currentTransactionCode, setCurrentTransactionCode] = useState<string>("");
        const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);


        const handleClickTransactionItemMenu = (transactionCode: string) => (event: React.MouseEvent<HTMLElement>) => {
            setAnchorEl(event.currentTarget);
            setCurrentTransactionCode(transactionCode);
        };

        const handleCloseMenuTraActions = () => {
            setAnchorEl(null);
        };

        const updateTransaction = (transaction: InputAccountTransaction) => {
            transactionService.update(transaction).then(() => {
                setNotificationMessage("Transação alterada com sucesso!")
                setStatusTransactionAction("success")
                setNotificationOpen(true);
            }).catch(() => {
                setNotificationMessage("Erro ao salvar a Transação!")
                setStatusTransactionAction("error")
                setNotificationOpen(true);
            })
        }

        const createTransaction = (transaction: InputAccountTransaction) => {
            transactionService.create(transaction).then(() => {
                setNotificationMessage("Transação criada com sucesso!")
                setStatusTransactionAction("success")
                setNotificationOpen(true);
            }).catch(() => {
                setNotificationMessage("Erro ao salvar a Transação!")
                setStatusTransactionAction("error")
                setNotificationOpen(true);
            })
        }

        const deleteTransaction = async (code: string) => {
            try {
                await transactionService.delete(code);
                setStatusTransactionAction("success");
                setNotificationMessage("Transação excluída com sucesso!");
            } catch (error) {
                setStatusTransactionAction("error");
                setNotificationMessage("Falha ao tentar excluir a transação!");
            } finally {
                setNotificationOpen(true);
            }
            reloadAccounts();
        }

        // Confirmação
        const [confirmOpen, setConfirmOpen] = useState(false);
        const [transactionCodeToDelete, setTransactionCodeToDelete] = useState("");

        const handleDelete = (code: string) => {
            transactionService.get(code).then((tran) => {
                setCurrentTransaction(tran)
                setConfirmOpen(true)
                handleCloseMenuTraActions();
            })

        };

        const handleConfirmDelete = () => {
            if (currentTransaction.code) {
                deleteTransaction(currentTransaction.code).then(r => loadTransactions());
                setConfirmOpen(false);
                setTransactionCodeToDelete("")
            }
        };


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
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>

                        <TableRow
                            style={{backgroundColor: '#f0f0f0'}}
                        >
                            <TableCell colSpan={5} align="left">
                                <b style={{marginRight: 10, color: '#444'}}>Saldo do mês anterior: </b>
                            </TableCell>
                            <TableCell colSpan={1} align="right"
                                       style={{
                                           color: lastMonthBalance < 0 ? red_color : green_color,
                                       }}
                            >
                                <b>{currencyFormatter.format(lastMonthBalance)}</b>
                            </TableCell>
                            <TableCell colSpan={1} align="right"></TableCell>

                        </TableRow>

                        <TableRow
                            style={{backgroundColor: '#fff', height: 30}}
                        >
                            <TableCell colSpan={7} align="right"></TableCell>
                        </TableRow>

                        {Array.from(groupedTransaction.keys()).map(date => {
                            const transactions = groupedTransaction.get(date);
                            if (!transactions) return null;

                            let saldo = 0.0;
                            if (transactionTotalsByDate.get(date))
                                saldo = transactionTotalsByDate.get(date) as number

                            return (
                                <React.Fragment key={date}>
                                    {transactions.map(transaction => (
                                        <TableRow key={`row-${transaction.code}`}
                                                  style={selectedTransactions.has(transaction.code) ? selectedRowStyle : undefined}
                                        >
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
                                                    alignItems: 'center',
                                                    color: transaction.value < 0 ? red_color : green_color
                                                }}
                                            >
                                                {`${currencyFormatter.format(transaction.value)}`}
                                            </TableCell>
                                            <TableCell
                                                align="right"
                                                style={{width: '24px'}}
                                            >
                                                <IconButton
                                                    key={transaction.code}
                                                    onClick={handleClickTransactionItemMenu(transaction.code)}
                                                >
                                                    <MoreVertIcon/>
                                                </IconButton>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                    <TableRow
                                        style={{backgroundColor: '#f0f0f0'}}
                                    >
                                        <TableCell colSpan={5} align="right"></TableCell>
                                        <TableCell colSpan={2} align="right"
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
                                        <TableCell colSpan={7} align="right"></TableCell>
                                    </TableRow>

                                </React.Fragment>
                            )
                        })}


                    </TableBody>
                </Table>

                <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleCloseMenuTraActions}
                >
                    <MenuItem
                        onClick={() => handleEditTransaction(currentTransactionCode)}
                    >Editar</MenuItem>
                    <MenuItem
                        onClick={() => handleDelete(currentTransactionCode)}
                    >Excluir</MenuItem>
                </Menu>

                <AccountTransactionDialogForm
                    transaction={currentTransaction}
                    setTransaction={setCurrentTransaction}
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
                    onClick={selectedTransactions.size > 0 ? removeTransaction : handleAddTransaction}
                >
                    {selectedTransactions.size > 0 ? <DeleteIcon/> : <AddIcon/>}
                </Fab>
                <Fab
                    color="primary"
                    aria-label="Import"
                    style={{
                        margin: '20px 0',
                        position: 'fixed',
                        bottom: '80px',
                        right: '30px',
                        height: '36px',
                        width: '36px'
                    }}
                    onClick={handleOpenDialog}
                >
                    <CloudUploadIcon/>
                </Fab>

                <Dialog
                    open={confirmOpen}
                    onClose={() => setConfirmOpen(false)}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                >
                    <DialogTitle id="alert-dialog-title">
                        {"Confirmar exclusão"}
                    </DialogTitle>
                    <DialogContent>
                        <DialogContentText id="alert-dialog-description">
                            Tem certeza de que deseja excluir?
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setConfirmOpen(false)} color="primary">
                            Cancelar
                        </Button>
                        <Button onClick={handleConfirmDelete} color="primary" autoFocus>
                            Confirmar
                        </Button>
                    </DialogActions>
                </Dialog>

                <UploadDialog 
                    open={dialogUploadOpen} 
                    setOpen={setDialogUploadOpen} 
                    aria-labelledby="form-dialog-title" 
                />
            

            </React.Fragment>
        )
            ;
    }

export default TransactionTable;