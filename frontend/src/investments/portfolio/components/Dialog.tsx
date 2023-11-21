import React, { FormEvent, useState, useEffect } from "react";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { Box } from "@mui/material";
import { Portfolio } from "../models";


interface FormErrors {
    name?: string;
}

interface FormDialogInterface {
    openDialog: boolean;
    setDialogOpen: (open: boolean) => void;
    sendPortfolio: (portfolio: Portfolio) => void;
    portfolio: Portfolio;
}

const FormDialogPortfolio: React.FC<FormDialogInterface> = ({
     openDialog, setDialogOpen, sendPortfolio, portfolio 
    }) => {
    
    const [code, setCode] = useState<string>("");
    const [name, setName] = useState<string>("");
    const [errors, setErrors] = useState<FormErrors>({});
    const [description, setDescription] = useState<string>("");

    useEffect(() => {
        setName(portfolio?.name || "");
        setDescription(portfolio?.description || "");
        setCode(portfolio?.code || "");
    }, [portfolio]);

    const handleFormSubmit = (e: FormEvent) => {
        e.preventDefault();
        sendPortfolio({
            name: name,
            description: description,
            code: code
        });
        setCode("");
        setName("");
        setDescription("");
    };

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.name = name ? "" : "O campo nome é obrigatório";
    
        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    
    const handleCancel = () => {        
        setDialogOpen(false);
        setCode("");
        setName("");
        setDescription("");
        setErrors({});
    };

    const handleClose = () => {
        if (validate()) {
            setDialogOpen(false);
        }
    };

    const preFormSubmit = (event: FormEvent) => {
        event.preventDefault();
        if (validate()) {
            handleFormSubmit(event)
        }
    };

    return (
        <Dialog open={openDialog} onClose={handleClose}>
            <DialogTitle>{portfolio.id ? "Edição de " : "Novo "}Portifólio</DialogTitle>
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
                        <DialogContentText
                            style={{ marginBottom: '1rem' }}>
                            Um portfólio é uma coleção diversificada de ativos financeiros,
                            como ações, títulos e fundos.
                        </DialogContentText>

                        <TextField
                            disabled
                            autoFocus
                            label="Código"
                            id="nameTextField"
                            variant="outlined"
                            fullWidth
                            value={code}
                            onChange={(e) => setName(e.target.value)}
                        />

                        <TextField
                            autoFocus
                            label="Nome"
                            id="nameTextField"
                            variant="outlined"
                            fullWidth
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            error={Boolean(errors.name)}
                            helperText={errors.name || ""}
                        />
                        <TextField
                            label="Descrição"
                            variant="outlined"
                            fullWidth
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                        />
                    </div>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCancel}>Cancel</Button>
                    <Button onClick={handleClose} type="submit">Salvar</Button>
                </DialogActions>
            </Box>

        </Dialog>

    );
}

export default FormDialogPortfolio;