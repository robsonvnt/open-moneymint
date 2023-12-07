import React, {useState} from "react";
import Paper from '@mui/material/Paper';
import {
    Backdrop,
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    IconButton,
    List,
    ListItem,
    ListItemSecondaryAction,
    ListItemText,
    Table
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import UpdateIcon from '@mui/icons-material/Update';
import {Portfolio} from "../models";
import InvestmentsService from "../../investments/InvestmentsService";
import {Warning as WarningIcon} from "@mui/icons-material";


interface TabelaProps {
    portfolios: Portfolio[];
    aoSelecionar: (portfolio: Portfolio) => void;
    deletePortifolio: (portfolio: Portfolio) => void;
    selectPortfolio: (portfolio: Portfolio) => void;
}

const PortfolioList: React.FC<TabelaProps> =
    ({
         portfolios, aoSelecionar, deletePortifolio, selectPortfolio
     }) => {

        const [loading, setLoading] = useState(false);
        const [successDialogOpen, setSuccessDialogOpen] = useState(false);
        const [message, setMessage] = useState('');

        const updatePrices = (portfolio: Portfolio) => {
            setLoading(true);
            try {
                if (portfolio.code)
                    InvestmentsService.updateAllInvestmentStockPrice(portfolio.code)
                setMessage('Preço das ações atualizados com sucesso!');
                setSuccessDialogOpen(true);
            } catch (error) {
                setMessage('Erro ao atualizar preços das ações.');
            } finally {
                setLoading(false);
            }
        }

        const handleDialogClose = () => {
            setSuccessDialogOpen(false);
        };

        // Confirmação
        const [confirmOpen, setConfirmOpen] = useState(false);
        const [currentPortfolio, setCurrentPortfolio] = useState<Portfolio>();

        const handleDelete = (portfolio: Portfolio) => {
            setCurrentPortfolio(portfolio);
            setConfirmOpen(true);
        }
        const handleConfirmDelete = () => {
            if (currentPortfolio) {
                deletePortifolio(currentPortfolio);
                setConfirmOpen(false);
            }
        };

        return (
            <div>
                <Backdrop open={loading}
                          style={{zIndex: 1201}}> {/* zIndex deve ser alto para cobrir todos os elementos */}
                    <CircularProgress color="inherit"/>
                </Backdrop>
                <Dialog open={successDialogOpen} onClose={handleDialogClose}>
                    <DialogContent>
                        {message}
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleDialogClose}>OK</Button>
                    </DialogActions>
                </Dialog>
                <Paper elevation={2}
                >
                    <List>
                        {portfolios.map((portfolio, indice) => (
                            <ListItem key={indice}
                                      className="hoverable-row"
                                      style={{cursor: 'pointer'}}
                                      onClick={() => selectPortfolio(portfolio)}
                            >
                                <ListItemText
                                    primary={portfolio.name}
                                    secondary={portfolio.description || "N/A"}
                                />
                                <ListItemSecondaryAction>
                                    <IconButton edge="end" aria-label="update"
                                                onClick={(e) => {
                                                    e.stopPropagation(); // Prevenir propagação
                                                    updatePrices(portfolio);
                                                }}
                                                style={{marginRight: '1px'}}
                                    >
                                        <UpdateIcon/>
                                    </IconButton>
                                    <IconButton edge="end" aria-label="edit"
                                                onClick={() => aoSelecionar(portfolio)}
                                                style={{marginRight: '1px'}}
                                    >
                                        <EditIcon/>
                                    </IconButton>
                                    <IconButton edge="end" aria-label="delete"
                                                onClick={() => handleDelete(portfolio)}>
                                        <DeleteIcon/>
                                    </IconButton>
                                </ListItemSecondaryAction>
                            </ListItem>
                        ))}
                    </List>

                    <Dialog
                        open={confirmOpen}
                        onClose={() => setConfirmOpen(false)}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">
                            <WarningIcon style={{color: 'red', verticalAlign: 'middle', marginRight: 10}}/>
                            {"Confirmar exclusão"}
                        </DialogTitle>
                        <DialogContent>

                            <DialogContentText id="alert-dialog-description">
                                <WarningIcon style={{color: 'red', verticalAlign: 'middle', marginRight: 10}}/>
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

                </Paper>
            </div>

        );
    };

export default PortfolioList;
