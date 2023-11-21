import React, { FormEvent, useState } from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { Box } from "@mui/material";
import { AssetType, Investment } from "../investments/models";
import { TransactionService } from "./TransactionService";
import { NewTransaction } from "./models";



interface FormErrors {
    type?: string;
    date?: string;
    quantity?: string;
    price?: string;
}

interface FormDialogTransactionInterface {
    openFormDialogTransaction: boolean;
    setOpenFormDialogTransaction: (open: boolean) => void;
    portfolioCode: string;
    investment: Investment;
    reloadTransactions: () => void;
    reloadInvestments: () => void;
}

const FormDialogTransaction: React.FC<FormDialogTransactionInterface> = ({
    openFormDialogTransaction,
    setOpenFormDialogTransaction,
    portfolioCode,
    investment,
    reloadTransactions,
    reloadInvestments
}) => {

    const [type, setType] = useState<string>("");
    const [date, setDate] = useState<string>("");
    const [quantity, setQuantity] = useState<number>(0);
    const [price, setPrice] = useState<number>(0);

    const [errors, setErrors] = useState<FormErrors>({});

    const sendTransaction = (new_transaction: NewTransaction) => {
        if (investment.code) {
            TransactionService.create(portfolioCode, investment.code, new_transaction)
            setOpenFormDialogTransaction(false);
        }
    }


    const handleFormSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (investment.code) {
            sendTransaction({
                investment_code: investment.code,
                type: type,
                date: date,
                quantity: quantity,
                price: price,
            });
            setType("");
            setDate("");
            setQuantity(0);
            setPrice(0);
        }
    };

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.type = type ? "" : "Tipo é obrigatório";
        tempErrors.date = date ? "" : "Data é obrigatório";
        tempErrors.quantity = quantity != 0 ? "" : "Quantidade é obrigatório";
        tempErrors.price = price != 0 ? "" : "Preço é obrigatório";

        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    const handleClose = () => {
        if (validate()) {
            setOpenFormDialogTransaction(false);
        }
    };

    const cancel = () => {
        setType("");
        setDate("");
        setQuantity(0);
        setPrice(0);
        setOpenFormDialogTransaction(false);
        setTimeout(() => {
            let tempErrors: FormErrors = {};
            setErrors(tempErrors);
        }, 200);
    };

    const preFormSubmit = (event: FormEvent) => {
        event.preventDefault();
        if (validate()) {
            handleFormSubmit(event);
            setTimeout(() => {
                reloadTransactions();
                reloadInvestments();
            }, 100);

        }
    };

    if (investment.asset_type === AssetType.FIXED_INCOME && quantity == 0) {
        setQuantity(1);
    }

    return (
        <Dialog open={openFormDialogTransaction} onClose={handleClose}>
            <DialogTitle>Nova Transação</DialogTitle>
            <Box
                onSubmit={preFormSubmit}
                component="form"
                sx={{
                    '& .MuiTextField-root': { m: 1 },
                }}
                noValidate
                autoComplete="off"
            >
                <DialogContent>
                    <div>
                        <TextField
                            margin="dense"
                            id="typeTextField"
                            select
                            label="Tipo de transação"
                            fullWidth
                            SelectProps={{
                                native: true,
                            }}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            required
                            value={type}
                            onChange={(e) => setType(e.target.value)}
                            error={Boolean(errors.type)}
                            helperText={errors.type || ""}
                        >
                            <option value="" disabled>Selecione um valor</option>

                            {investment.asset_type === "FIXED_INCOME" ? (
                                <>
                                    <option value="INTEREST">Rendimento</option>
                                    <option value="WITHDRAWAL">Saque</option>
                                    <option value="DEPOSIT">Depósito</option>
                                </>
                            ) : (
                                <>
                                    <option value="BUY">Compra</option>
                                    <option value="SELL">Venda</option>
                                </>
                            )}


                        </TextField>

                        <TextField
                            autoFocus
                            label="Data da transação"
                            id="dateTextField"
                            type="date"
                            InputLabelProps={{
                                shrink: true,
                            }}
                            fullWidth
                            required
                            value={date}
                            onChange={(e) => setDate(e.target.value)}
                            error={Boolean(errors.date)}
                            helperText={errors.date || ""}
                        />


                        {investment.asset_type !== AssetType.FIXED_INCOME && (
                            <TextField autoFocus
                                label="Quantidade"
                                id="quantityTextField"
                                type="number"
                                variant="outlined"
                                fullWidth
                                value={quantity}
                                onChange={(e) => setQuantity(parseInt(e.target.value))}
                                error={Boolean(errors.quantity)}
                                helperText={errors.quantity || ""}
                            />
                        )}


                        <TextField
                            autoFocus
                            label="Preço"
                            id="priceTextField"
                            type="number"
                            variant="outlined"
                            fullWidth
                            value={price}
                            onChange={(e) => setPrice(parseFloat(e.target.value))}
                            error={Boolean(errors.price)}
                            helperText={errors.price || ""}
                        />

                    </div>
                </DialogContent>
                <DialogActions>
                    <Button onClick={cancel}>Cancel</Button>
                    <Button onClick={handleClose} type="submit">Salvar</Button>
                </DialogActions>
            </Box>

        </Dialog>

    );
}

export default FormDialogTransaction;