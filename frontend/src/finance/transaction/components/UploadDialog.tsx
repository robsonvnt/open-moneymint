import React, {useEffect, useState} from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import {TransactionService} from "../TransactionService";
import {wait} from "@testing-library/user-event/dist/utils";
import {AccountService} from "../../account/AccountService";
import {Grid, InputLabel, Select, SelectChangeEvent} from "@mui/material";
import MenuItem from "@mui/material/MenuItem";
import {AccountModel} from "../../models";
import TextField from "@mui/material/TextField";

interface UploadDialogProps {
    open: boolean;
    setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}

const UploadDialog: React.FC<UploadDialogProps> = ({open, setOpen}) => {

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [selectedAccount, setSelectedAccount] = useState<string>('');
    const [allAccounts, setAllAccounts] = useState<AccountModel[]>([]); // Estado para armazenar as contas

    useEffect(() => {
        AccountService.getAllAccounts().then(accounts => {
            setAllAccounts(accounts);
        }).catch(error => {
            console.error("Erro ao carregar as contas:", error);
        });
    }, []);

    const handleClose = () => {
        setOpen(false);
        setSelectedFile(null); // Limpa o arquivo selecionado ao fechar
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (selectedFile) {

            // const formData = new FormData();
            // formData.append('file', selectedFile);

            let uploaded = await TransactionService.uploadTransactionsFile(selectedAccount, selectedFile)
            handleClose(); // Fecha o diálogo após o envio (ou em caso de falha)

        }
    };

    return (
        <div>
            <Button variant="outlined" onClick={() => setOpen(true)}>
                Upload File
            </Button>
            <Dialog
                open={open}
                onClose={handleClose}
                aria-labelledby="form-dialog-title"
                sx={{'& .MuiDialog-paper': {width: '500px', maxWidth: 'none'}}}
            >
                <DialogTitle id="form-dialog-title">
                    Upload File
                    <IconButton
                        aria-label="close"
                        onClick={handleClose}
                        sx={{
                            position: 'absolute',
                            right: 8,
                            top: 8,
                            color: (theme) => theme.palette.grey[500],
                        }}
                    >
                        <CloseIcon/>
                    </IconButton>
                </DialogTitle>
                <DialogContent>
                    <Grid item xs={12} sm={6}>
                        <Grid item>

                            <TextField
                                margin="dense"
                                id="asset_type"
                                select
                                label="Selecione a conta para importar o extrato"
                                fullWidth
                                SelectProps={{
                                    native: true,
                                }}
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                required
                                value={selectedAccount}
                                onChange={(e) => setSelectedAccount(e.target.value)}
                            >
                                <option value="" disabled>Escolha uma conta</option>
                                {allAccounts.map((account: AccountModel) => (
                                    <option value={account.code}>{account.name}</option>
                                ))}

                            </TextField>

                        </Grid>

                        <Grid item>
                            <input
                                accept=".txt"
                                style={{display: 'none'}}
                                id="raised-button-file"
                                multiple
                                type="file"
                                onChange={handleFileChange}
                            />
                            <label htmlFor="raised-button-file">
                                <Button component="span">
                                    Select File
                                </Button>
                            </label>
                            {selectedFile && <p>File: {selectedFile.name}</p>}
                        </Grid>
                    </Grid>

                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleUpload} color="primary" disabled={!selectedFile}>
                        Upload
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}

export default UploadDialog;
