import React, {useEffect, useState} from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import {
    AccountModel,
    AccountTransactionType,
    CategoryModel, CategoryTreeItem,
    getTransactionTypeLabel,
    NewAccountTransaction
} from "../../models";
import {InputAdornment} from "@mui/material";
import MenuItem from "@mui/material/MenuItem";
import {Grid} from "@mui/material";
import {AccountService} from "../../account/AccountService";
import {CategoryService} from "../../category/CategoryService";

interface AccountTransactionDialogFormProps {
    open: boolean;
    onClose: () => void;
    onSave: (transaction: NewAccountTransaction) => void;
}

interface FormErrors {
    account_code?: string,
    description?: string,
    category_code?: string,
    type?: string,
    date?: string,
    value?: string
}

const AccountTransactionDialogForm: React.FC<AccountTransactionDialogFormProps> = ({open, onClose, onSave}) => {
    const [transaction, setTransaction] = useState<NewAccountTransaction>({});
    const [accountList, setAccountList] = React.useState<AccountModel[]>([]);
    const [categoryList, setCategoryList] = React.useState<CategoryTreeItem[]>([]);

    const accountService = AccountService;
    const categoryService = CategoryService;

    const prepareCategoryList = (parentName: string, categoryList: CategoryTreeItem[]): CategoryTreeItem[] => {
        let newCategoryList: CategoryTreeItem[] = [];
        categoryList.map(category => {
            let newCategory: CategoryTreeItem = {
                code: category.code,
                name: parentName != "" ? `${parentName} > ${category.name}` : category.name,
                children: []
            }
            newCategoryList.push(newCategory)
            if (category.children.length > 0) {
                let childrenItems = prepareCategoryList(newCategory.name, category.children);
                childrenItems.map(cat => {
                    newCategoryList.push(cat)
                })
            }
        })
        return newCategoryList;
    };

    useEffect(() => {
        accountService.getAllAccounts()
            .then(accountList => {
                setAccountList(accountList);
            });

        categoryService.getAllCategories()
            .then(categoryList => {
                let newCategoryList = prepareCategoryList("", categoryList);
                setCategoryList(newCategoryList);
            });

    }, [open]);

    const clearForm = () => {
        setTransaction({})
        setErrors({})
    }

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {

        let transactionType = event.target.name === "type" ? event.target.value : transaction.type;
        let transactionValue = event.target.name === "value" ? parseFloat(event.target.value) : transaction.value ? transaction.value : 0.0;
        if (transactionType === AccountTransactionType.DEPOSIT) {
            transactionValue = Math.abs(transactionValue);
        } else if (transactionType === AccountTransactionType.TRANSFER || transactionType === AccountTransactionType.WITHDRAWAL) {
            transactionValue = Math.abs(transactionValue) * -1;
        }
        setTransaction({...transaction, [event.target.name]: event.target.value, "value": transactionValue});

    };

    const handleSave = () => {
        if (validate()) {
            onSave(transaction);
            onClose();
            clearForm();
        }
    };

    const handleClose = () => {
        onClose();
        clearForm();
    };

    const transactionOptions = Object.keys(AccountTransactionType).map(key => {
        return {
            value: AccountTransactionType[key as keyof typeof AccountTransactionType],
            label: getTransactionTypeLabel(key)
        };
    });

    // Validation

    const [errors, setErrors] = useState<FormErrors>({});

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.account_code = transaction.account_code ? "" : "Campo é obrigatório";
        tempErrors.type = transaction.type ? "" : "Campo é obrigatório";
        tempErrors.description = transaction.description ? "" : "Campo é obrigatório";
        tempErrors.date = transaction.date ? "" : "Campo é obrigatório";
        if (transaction.value)
            tempErrors.value = transaction.value > 0 ? "" : "Valor deve ser maior que zero.";
        else
            tempErrors.value = "Campo é obrigatório"

        if (transaction.type === AccountTransactionType.TRANSFER || transaction.type === AccountTransactionType.WITHDRAWAL) {
            if (transaction.value) {
                tempErrors.value = transaction.value < 0 ? "" : "O valor deve ser negativo";
            } else {
                tempErrors.value = "Campo é obrigatório";
            }
        } else {
            tempErrors.value = transaction.value ? "" : "Campo é obrigatório";
        }

        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>Adicionar Nova Transação</DialogTitle>
            <DialogContent>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={6}>
                        <TextField
                            select
                            margin="dense"
                            name="account_code"
                            label="Conta"
                            required
                            value={transaction.account_code}
                            error={Boolean(errors.account_code)}
                            helperText={errors.account_code || ""}
                            onChange={(e) =>
                                setTransaction({
                                    ...transaction,
                                    account_code: e.target.value,
                                })}
                            fullWidth
                        >
                            {accountList.map((option) => (
                                <MenuItem key={option.code} value={option.code}>
                                    {option.name}
                                </MenuItem>
                            ))}

                        </TextField>

                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            margin="dense"
                            name="description"
                            label="Descrição"
                            type="text"
                            required
                            fullWidth
                            value={transaction.description}
                            error={Boolean(errors.description)}
                            helperText={errors.description || ""}
                            onChange={handleChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            select
                            margin="dense"
                            name="type"
                            label="Tipo"
                            required
                            value={transaction.type}
                            error={Boolean(errors.type)}
                            helperText={errors.type || ""}
                            onChange={handleChange}
                            fullWidth
                        >
                            {transactionOptions.map((option) => (
                                <MenuItem key={option.value} value={option.value}>
                                    {option.label}
                                </MenuItem>
                            ))}

                        </TextField>
                    </Grid>
                    <Grid item xs={12} sm={6}>

                        <TextField
                            select
                            margin="dense"
                            name="category_code"
                            label="Categoria"
                            value={transaction.category_code}
                            error={Boolean(errors.category_code)}
                            helperText={errors.category_code || ""}
                            onChange={(e) =>
                                setTransaction({
                                    ...transaction,
                                    category_code: e.target.value,
                                })}
                            fullWidth
                        >
                            {categoryList.map((option) => (
                                <MenuItem key={option.code} value={option.code}>
                                    {option.name}
                                </MenuItem>
                            ))}

                        </TextField>

                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            margin="dense"
                            name="date"
                            label="Data"
                            type="date"
                            required
                            fullWidth
                            InputLabelProps={{shrink: true}}
                            value={transaction.date}
                            error={Boolean(errors.date)}
                            helperText={errors.date || ""}
                            onChange={handleChange}
                        />

                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            margin="dense"
                            name="value"
                            label="Valor"
                            type="number"
                            fullWidth
                            required
                            InputProps={{
                                startAdornment: <InputAdornment position="start">R$</InputAdornment>,
                            }}
                            value={transaction.value}
                            error={Boolean(errors.value)}
                            helperText={errors.value || ""}
                            onChange={handleChange}
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

export default AccountTransactionDialogForm;
