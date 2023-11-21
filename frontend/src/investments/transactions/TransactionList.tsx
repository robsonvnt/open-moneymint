import React, { FormEvent, useState, useEffect } from "react";
import { BottomNavigation, BottomNavigationAction, Box, Button, Checkbox, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Divider, List, ListItem, ListItemText, Typography } from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import RefreshIcon from '@mui/icons-material/Refresh';
import { green, red } from '@mui/material/colors';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import { TransactionModel } from "./models";
import { TransactionService } from "./TransactionService";
import FormDialogTransaction from "./TransactionDialogForm";
import { Investment } from "../investments/models";
import { Portfolio } from "../portfolio/models";
import { currencyFormatter, formatDateStr } from "../../helpers/BRFormatHelper";


interface TransactionListInterface {
    investment: Investment;
    portfolio: Portfolio;
    reloadInvestments: () => void;
}

const TransactionList: React.FC<TransactionListInterface> = ({
    investment,
    portfolio,
    reloadInvestments
}) => {

    const [transactions, setTransactions] = useState<TransactionModel[]>([]);
    const service = TransactionService;

    // List transactions

    const loadTransaction = () => {
        if (portfolio.code && investment.code) {
            service.getAllTransactions(portfolio.code, investment.code)
                .then(
                    transactions => setTransactions(transactions)
                )
        } else {
            setTransactions([])
        }
    }

    useEffect(() => {
        loadTransaction();
    }, []);

    const [selectedItems, setSelectedItems] = useState<(string | string)[]>([]);

    const handleCheckboxChange = (itemCode: string | string) => {
        if (selectedItems.includes(itemCode)) {
            setSelectedItems(selectedItems.filter(id => id !== itemCode));
        } else {
            setSelectedItems([...selectedItems, itemCode]);
        }
    };


    // Delete Transaction
    const [confirmDeleteTransaction, setConfirmDeleteTransaction] = useState(false);

    const onClickDeleteTransaction = () => {
        setConfirmDeleteTransaction(true);
    };

    const getAssetTypeLabel = (key: string) => {
        const assetType: {
            BUY: string;
            SELL: string;
            INTEREST: string;
            WITHDRAWAL: string;
            DEPOSIT: string;
        } = {
            BUY: "Compra",
            SELL: "Venda",
            INTEREST: "Juros",
            WITHDRAWAL: "Retirada",
            DEPOSIT: "Depósito",
        };
        // Explicitly cast the key to a valid property name
        return assetType[key as 'BUY' | 'SELL' | 'INTEREST' | 'WITHDRAWAL' | 'DEPOSIT'];
    };

    const deleteTransactions = () => {
        for (let i = 0; i < selectedItems.length; i++) {
            if (portfolio.code && investment.code) {
                service.delete(portfolio.code, investment.code, selectedItems[i])
            }
        }
        setSelectedItems([]);
        setConfirmDeleteTransaction(false);
        setTimeout(() => {
            loadTransaction();
            reloadInvestments();
        }, 100);
    }



    // NewTransactionDIalog

    const [openFormDialogTransaction, setOpenFormDialogTransaction] = useState<boolean>(false);

    const openNewTransactionDIalog = () => {
        setOpenFormDialogTransaction(true);
    }



    return (
        <>
            <Box width={'100%'}>

                <List sx={{
                    width: '100%',
                    bgcolor: 'background.paper',
                    marginBottom: '30px'
                }}
                >
                    {transactions.map((transaction) => (
                        <React.Fragment key={transaction.code}>
                            <ListItem
                                alignItems="flex-start"
                                secondaryAction={
                                    <Checkbox
                                        edge="end"
                                        inputProps={{ 'aria-labelledby': `checkbox-list-label-${transaction.code}` }}
                                        onChange={() => handleCheckboxChange(transaction.code)}
                                        checked={selectedItems.includes(transaction.code)}
                                    />
                                }
                            >

                                {transaction.type === 'SELL' || transaction.type === 'WITHDRAWAL' ? (
                                    <ArrowDownwardIcon style={{ color: red[500], marginRight: 8, marginTop: 46 }} />
                                ) : (
                                    <ArrowUpwardIcon style={{ color: green[500], marginRight: 8, marginTop: 46 }} />
                                )}
                                <ListItemText
                                    primary={getAssetTypeLabel(transaction.type)}
                                    secondary={
                                        <React.Fragment>
                                            <Typography
                                                sx={{ display: 'inline' }}
                                                component="span"
                                                variant="body2"
                                                color="text.primary"
                                            >
                                                Data: <b>{formatDateStr(transaction.date)}</b>
                                            </Typography>
                                            <br />
                                            Quantidade: <b>{transaction.quantity}</b>
                                            <br />
                                            Valor Unitário: <b>{currencyFormatter.format(transaction.price)}</b>
                                            <br />
                                            Valor total: <b>{currencyFormatter.format(transaction.quantity * transaction.price)}</b>
                                        </React.Fragment>
                                    }
                                />
                            </ListItem>
                            <Divider variant="fullWidth" component="li" />
                        </React.Fragment>
                    ))}

                </List>
                <BottomNavigation
                    style={{
                        position: 'absolute', // Posicionamento absoluto
                        bottom: 0, // Alinhado na parte inferior
                        left: 0, // Alinhado à esquerda
                        right: 0, // Alinhado à direita
                        width: '100%', // Largura total
                    }}
                >
                    <BottomNavigationAction
                        label="Recents"
                        value="recents"
                        icon={<RefreshIcon />}
                        style={{
                            color: '#4d4d4d'
                        }}
                        onClick={loadTransaction}
                    />
                    <BottomNavigationAction
                        label="Recents"
                        value="recents"
                        onClick={openNewTransactionDIalog}
                        icon={<AddIcon />}
                        style={{
                            color: '#4d4d4d'
                        }}
                    />
                    <BottomNavigationAction
                        label="Favorites"
                        value="favorites"
                        icon={<DeleteIcon />}
                        disabled={selectedItems.length === 0}
                        style={{
                            color: selectedItems.length > 0 ? '#4d4d4d' : '#ddd'
                        }}
                        onClick={onClickDeleteTransaction}
                    />
                </BottomNavigation>

            </Box>

            <FormDialogTransaction
                openFormDialogTransaction={openFormDialogTransaction}
                setOpenFormDialogTransaction={setOpenFormDialogTransaction}
                portfolioCode={portfolio.code ? portfolio.code : ""}
                investment={investment}
                reloadTransactions={loadTransaction}
                reloadInvestments={reloadInvestments}
            />


            <Dialog
                open={confirmDeleteTransaction}
                onClose={() => setConfirmDeleteTransaction(false)}
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
                    <Button onClick={() => setConfirmDeleteTransaction(false)} color="primary">
                        Cancelar
                    </Button>
                    <Button onClick={deleteTransactions} color="primary" autoFocus>
                        Confirmar
                    </Button>
                </DialogActions>
            </Dialog>

        </>
    );
}

export default TransactionList;