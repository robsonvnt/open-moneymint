import React, { FormEvent, useState, useEffect } from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { Box, DialogContentText, Grid, Link, Tab, Tabs } from "@mui/material";
import { Portfolio } from "../../portfolio/models";
import { AssetType, Investment } from "../models";
import TransactionList from "../../transactions/TransactionList";


interface FormErrors {
    asset_type?: string;
    ticker?: string;
    quantity?: string;
    purchase_price?: string;
    purchase_date?: string;
}

interface InvestmentFormDialogI {
    dialogOpen: boolean;
    setDialogOpen: (open: boolean) => void;
    portfolio: Portfolio;
    investment: Investment;
    setInvestment: (investment: Investment) => void;
    handleFormSubmit: (event: React.FormEvent) => void;
    deleteInvestment: (code: string) => void;
    activeTab: number;
    setActiveTab: (active: number) => void;
    reloadInvestments: () => void;
}

const FormDialogPortfolio: React.FC<InvestmentFormDialogI> = ({
    dialogOpen,
    setDialogOpen,
    portfolio,
    investment,
    setInvestment,
    handleFormSubmit,
    deleteInvestment,
    activeTab,
    setActiveTab,
    reloadInvestments
}) => {

    const [confirmOpen, setConfirmOpen] = useState(false);
    const [errors, setErrors] = useState<FormErrors>({});

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.ticker = investment.ticker ? "" : "Este campo é obrigatório";
        tempErrors.quantity = investment.quantity > 0 ? "" : "A quantidade deve ser maior que zero";
        tempErrors.purchase_price = investment.purchase_price > 0 ? "" : "O preço de compra deve ser maior que zero";
        tempErrors.purchase_date = investment.purchase_date ? "" : "A data de compra é obrigatória";
        tempErrors.asset_type = investment.asset_type ? "" : "O tipo do investimento é obrigatória";

        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    const preFormSubmit = (event: FormEvent) => {
        event.preventDefault();
        if (validate()) {
            handleFormSubmit(event)
        }
    };

    const activactivateTab = (newValue: number) => {
        setActiveTab(newValue);
        if (newValue == 1) {
            // loadTransaction();
        }
    }

    const onDialogClose = (open: boolean) => {
        setDialogOpen(open)
    }



    // Form  de Investment

    if (investment.asset_type === AssetType.FIXED_INCOME && investment.quantity == 0) {
        setInvestment({
            ...investment,
            quantity: 1,
        })
    }

    const handleConfirmDelete = () => {
        deleteInvestment(investment.code || "");
        setConfirmOpen(false);
    };


    return (
        <>

            <Dialog
                open={dialogOpen}
                onClose={() => onDialogClose(false)}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Dados do Investimento</DialogTitle>

                <DialogContent
                >
                    <Box
                        sx={{ borderBottom: 0, borderColor: 'divider' }}

                        style={{ minHeight: '34vh', maxHeight: '44vh', width: '100%' }}
                    >
                        <Tabs
                            value={activeTab}
                            onChange={(event, newValue) => activactivateTab(newValue)}
                            aria-label="abas de investimento"
                            sx={{
                                width: '100%',           // Por padrão, ocupa 100% da largura
                                maxWidth: '550px',       // Limita a largura máxima a 550px
                                '@media (min-width:600px)': { // Em telas acima de 600px
                                    width: '550px',      // Define a largura como 550px
                                },
                                marginBottom: 1
                            }}
                        // style={{width: '550px', maxWidth: }}
                        >
                            <Tab label="Detalhes" />
                            <Tab label="Transações" />
                        </Tabs>


                        {activeTab === 0 && (
                            <Box
                                onSubmit={preFormSubmit}
                                component="form"
                                noValidate
                                autoComplete="off"
                            >
                                <Grid
                                    style={{
                                        paddingBottom: '55px'
                                    }}
                                >

                                    <TextField
                                        margin="dense"
                                        id="portfolio_code"
                                        label="Código do Portfólio"
                                        type="text"
                                        value={investment.portfolio_code}
                                        InputProps={{
                                            readOnly: true,
                                        }}
                                        style={{ display: 'none' }}
                                    />


                                    {investment.code && ( // Esta linha verifica se há um valor em investment.code
                                        <Grid item xs={12} sm={6}>
                                            <TextField
                                                margin="dense"
                                                id="code"
                                                label="Código"
                                                type="text"
                                                value={investment.code}
                                                InputProps={{
                                                    readOnly: true,
                                                }}
                                                fullWidth
                                            />
                                        </Grid>
                                    )}

                                    <Grid item xs={12} sm={12}>
                                        <TextField
                                            margin="dense"
                                            id="asset_type"
                                            select
                                            label="Tipo de Ativo"
                                            fullWidth
                                            SelectProps={{
                                                native: true,
                                            }}
                                            InputLabelProps={{
                                                shrink: true,
                                            }}
                                            required
                                            value={investment.asset_type}
                                            onChange={(e) => setInvestment({
                                                ...investment,
                                                asset_type: e.target.value,
                                            })}
                                            error={Boolean(errors.asset_type)}
                                            helperText={errors.asset_type || ""}
                                        >
                                            <option value="" disabled>Selecione um valor</option>
                                            <option value="STOCK">Ações</option>
                                            <option value="REIT">FII</option>
                                            <option value="FIXED_INCOME">Renda Fixa</option>
                                        </TextField>

                                        <Grid container spacing={2} alignItems="center">
                                            <Grid item>
                                                <TextField
                                                    margin="dense"
                                                    id="ticker"
                                                    label="Ticker"
                                                    type="text"
                                                    fullWidth
                                                    required
                                                    value={investment.ticker}
                                                    onChange={(e) => setInvestment({
                                                        ...investment,
                                                        ticker: e.target.value,
                                                    })}
                                                    error={Boolean(errors.ticker)}
                                                    helperText={errors.ticker || ""}
                                                />
                                            </Grid>
                                            <Grid item>
                                                {(investment.asset_type === AssetType.STOCK || investment.asset_type === AssetType.REIT) && (
                                                    <Link
                                                        href={`https://statusinvest.com.br/acoes/${encodeURIComponent(investment.ticker)}`}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                    >
                                                        Ver no Status Invest
                                                    </Link>
                                                )}

                                            </Grid>
                                        </Grid>

                                        {investment.asset_type !== AssetType.FIXED_INCOME && (
                                            <TextField
                                                margin="dense"
                                                id="quantity"
                                                label="Quantidade"
                                                type="number"
                                                fullWidth
                                                required
                                                value={investment.quantity}
                                                onChange={(e) => setInvestment({
                                                    ...investment,
                                                    quantity: parseInt(e.target.value),
                                                })}
                                                error={Boolean(errors.quantity)}
                                                helperText={errors.quantity || ""}
                                            />
                                        )}
                                        <TextField
                                            margin="dense"
                                            id="purchase_price"
                                            label={investment.asset_type === AssetType.FIXED_INCOME ? "Valor aplicado" : "Preço de Compra"}
                                            type="number"
                                            fullWidth
                                            required
                                            value={investment.purchase_price}
                                            onChange={(e) => setInvestment({
                                                ...investment,
                                                purchase_price: parseFloat(e.target.value),
                                            })}
                                            error={Boolean(errors.purchase_price)}
                                            helperText={errors.purchase_price || ""}
                                        />
                                        <TextField
                                            margin="dense"
                                            id="purchase_date"
                                            label={investment.asset_type === AssetType.FIXED_INCOME ? "Dada do aplicação" : "Data de Compra"}
                                            type="date"
                                            InputLabelProps={{
                                                shrink: true,
                                            }}
                                            fullWidth
                                            required
                                            value={investment.purchase_date}
                                            onChange={(e) => setInvestment({
                                                ...investment,
                                                purchase_date: e.target.value,
                                            })}
                                            error={Boolean(errors.purchase_date)}
                                            helperText={errors.purchase_date || ""}
                                        />

                                        <TextField
                                            margin="dense"
                                            id="current_average_price"
                                            label={investment.asset_type === AssetType.FIXED_INCOME ? "Saldo Atual" : "Preço Médio Atual"}
                                            type="number"
                                            fullWidth
                                            value={investment.current_average_price}
                                            onChange={(e) => setInvestment({
                                                ...investment,
                                                current_average_price: parseFloat(e.target.value),
                                            })}
                                        />
                                    </Grid>
                                </Grid>
                                <DialogActions
                                    style={{
                                        position: 'absolute', // Posicionamento absoluto
                                        bottom: 0, // Alinhado na parte inferior
                                        right: 0, // Alinhado à direita
                                        width: '100%', // Largura total
                                        backgroundColor: 'white'
                                    }}
                                >
                                    <Grid container justifyContent="space-between">

                                        <Grid item>
                                            {investment.code && (
                                                <Button
                                                    onClick={() => setConfirmOpen(true)}
                                                    style={{ color: 'red', marginLeft: 20 }}
                                                >
                                                    Excluir
                                                </Button>
                                            )}
                                        </Grid>

                                        <Grid item>
                                            <Button onClick={() => setDialogOpen(false)} color="primary">
                                                Cancelar
                                            </Button>
                                            <Button type="submit" color="primary">
                                                Salvar
                                            </Button>
                                        </Grid>
                                    </Grid>
                                </DialogActions>
                            </Box>
                        )}

                        {activeTab === 1 && (
                            <Box width={'100%'}>
                                <TransactionList
                                    investment={investment}
                                    portfolio={portfolio}
                                    reloadInvestments={reloadInvestments}
                                />
                            </Box>
                        )}

                    </Box>
                </DialogContent>

            </Dialog>

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
                        Tem certeza de que deseja excluir este investimento?
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


        </>

    );
}

export default FormDialogPortfolio;