import React, {useState} from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Grid,
    InputAdornment
} from '@mui/material';
import {AccountTransactionType} from "../../models";

export interface NewAccountModel {
    name: string;
    description?: string;
    balance: number;
}

interface FormErrors {
    name?: string;
    description?: string;
    balance?: string;
}

interface AccountDialogFormProps {
    open: boolean;
    onClose: () => void;
    onSave: (account: NewAccountModel) => void;
}

const AccountDialogForm: React.FC<AccountDialogFormProps> = ({open, onClose, onSave}) => {
    const [newAccount, setNewAccount] = useState<NewAccountModel>({name: '', description: '', balance: 0});
    const [errors, setErrors] = useState<FormErrors>({});

    const clearForm = () => {
        setNewAccount({name: "", balance: 0});
        setErrors({});
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        let value: any = e.target.value;
        if (e.target.name === "balance"){
            value = parseFloat(value);
        }
        setNewAccount({...newAccount, [e.target.name]: value});
    };

    const handleClose = () => {
        onClose();
        clearForm()
    };

    const handleSave = () => {
        if (validate()) {
            onSave(newAccount);
            onClose();
            clearForm()
        }
    };

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.name = newAccount.name ? "" : "Campo é obrigatório";

        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Adicionar Nova Conta</DialogTitle>
            <DialogContent>

                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={6} sm={6}>
                        <TextField
                            autoFocus
                            margin="dense"
                            name="name"
                            label="Nome da instituição"
                            type="text"
                            fullWidth
                            value={newAccount.name}
                            onChange={handleChange}
                            error={Boolean(errors.name)}
                            helperText={errors.name || ""}
                        />
                    </Grid>
                    <Grid item xs={6} sm={6}>
                        <TextField
                            margin="dense"
                            name="description"
                            label="Descrição"
                            type="text"
                            fullWidth
                            value={newAccount.description}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            margin="dense"
                            name="balance"
                            label="Saldo inicial da conta"
                            type="number"
                            fullWidth
                            InputProps={{
                                startAdornment: <InputAdornment position="start">R$</InputAdornment>,
                            }}
                            value={newAccount.balance}
                            onChange={handleChange}
                            error={Boolean(errors.balance)}
                            helperText={errors.balance || ""}
                        />
                    </Grid>
                </Grid>


            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Cancelar</Button>
                <Button onClick={handleSave}>Salvar</Button>
            </DialogActions>
        </Dialog>
    );
};

export default AccountDialogForm;
