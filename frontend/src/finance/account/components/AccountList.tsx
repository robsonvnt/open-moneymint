import React, {useEffect, useState} from 'react';
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import List from "@mui/material/List";
import {Checkbox, Divider} from "@mui/material";
import {AccountModel} from "../../models";
import {AccountService} from "../AccountService";
import {currencyFormatter} from "../../../helpers/BRFormatHelper";
import IconButton from '@mui/material/IconButton';
import AddIcon from '@mui/icons-material/Add';
import AccountDialogForm, {InputAccountModel} from "./AccountDialogForm"; // Substitua por seu ícone preferido


interface AccountListProps {
    checked: Map<string, boolean>;
    setChecked: React.Dispatch<React.SetStateAction<Map<string, boolean>>>;
}


const AccountList: React.FC<AccountListProps> =
    ({
         checked,
         setChecked
     }) => {

        const [accountList, setAccountList] = React.useState<AccountModel[]>([]);
        const accountService = AccountService;
        const [totalBalance, setTotalBalance] = React.useState<number>(0.0);


        const handleToggle = (code: string) => () => {
            let newValue = !checked.get(code);
            const newCheckedMap = new Map(checked.entries());
            newCheckedMap.set(code, newValue);
            setChecked(newCheckedMap);
        };

        const updateList = (accounts: AccountModel[]) => {
            let tmpTotalBalance = 0
            accounts.map(account => {
                checked.set(account.code, true)
                tmpTotalBalance += account.balance
            });
            setTotalBalance(tmpTotalBalance)
            setAccountList(accounts);
        }

        useEffect(() => {
            if (accountList.length == 0) {
                accountService.getAllAccounts()
                    .then(accounts => {
                        updateList(accounts);
                    });
            }
        }, []);

        // New or Edit Account
        const [openForm, setOpenForm] = useState<boolean>(false);
        const [onCloseForm, setOnCloseForm] = useState<boolean>(false);
        const [onSaveAccount, setOnSaveAccount] = useState<boolean>(false);
        const [currentAccount, setCurrentAccount] = useState<InputAccountModel>({
            name: '',
            description: '',
            balance: 0
        });


        const handleIconClick = () => {
            setCurrentAccount({name: '', description: '', balance: 0})
            setOpenForm(true);
        };

        const handleItemListDoubleClick = (code: string) => {
            accountService.get(code).then((account) => {
                setCurrentAccount(account)
                setOpenForm(true);
            })
        };

        const handleDialogClose = () => {
            setOpenForm(false);
        };

        const handleOnDelete = (account: InputAccountModel) => {
            if (account.code) {
                accountService.delete(account.code)
                setOpenForm(false);
                setCurrentAccount({name: '', description: '', balance: 0})
                accountService.getAllAccounts()
                    .then(accounts => {
                        updateList(accounts);
                    });
            }
        }

        const handleOnSave = (account: InputAccountModel) => {
            if (account.code) {
                AccountService.update(account).then((updatedAccount) => {
                    let newAccountList: AccountModel[] = []
                    accountList.map((acc): void => {
                        if (acc.code === updatedAccount.code) {
                            newAccountList.push(updatedAccount)
                        } else {
                            newAccountList.push(acc)
                        }
                    })

                    updateList(newAccountList);
                })
            } else {
                AccountService.create(account).then((createdAccount) => {
                    let newAccountList: AccountModel[] = []
                    accountList.map((acc) => newAccountList.push(acc))
                    newAccountList.push(createdAccount);
                    updateList(newAccountList);
                })
            }
        };


        return (
            <>
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    margin: 0,
                    marginTop: 5
                }}>
                    <div style={{width: 48}}> {/* Ajuste a largura para corresponder à do IconButton */}
                    </div>
                    <h4 style={{
                        margin: 0,
                        flexGrow: 1,
                        textAlign: 'center'
                    }}>
                        Contas
                    </h4>
                    <IconButton onClick={handleIconClick}>
                        <AddIcon/> {/* Substitua por seu ícone preferido */}
                    </IconButton>
                </div>

                <List dense
                      sx={{width: '100%', maxWidth: 360, bgcolor: 'background.paper'}}
                      style={{paddingTop: 2, paddingBottom: 20}}

                >
                    {accountList.map((account) => {
                        const labelId = `checkbox-list-secondary-label-${account.code}`;
                        return (
                            <ListItem
                                key={account.code}

                                secondaryAction={

                                    <Checkbox
                                        edge="end"
                                        onChange={handleToggle(account.code)}
                                        checked={checked.get(account.code)}
                                        inputProps={{'aria-labelledby': labelId}}
                                    />
                                }
                                disablePadding
                            >
                                <ListItemButton onDoubleClick={() => handleItemListDoubleClick(account.code)}>
                                    <ListItemText id={labelId} primary={`${account.name}`}/>
                                    <div style={{
                                        display: 'flex',
                                        alignItems: 'center',
                                        color: account.balance < 0 ? '#db0000' : 'inherit' // Altera a cor para vermelho se o saldo for negativo
                                    }}>
                                        <ListItemText id={labelId}
                                                      primary={`${currencyFormatter.format(account.balance)}`}/>
                                    </div>
                                </ListItemButton>
                            </ListItem>
                        );
                    })}
                    {/*<Divider light/>*/}
                    <ListItem disablePadding style={{backgroundColor: "#f0f0f0"}}>
                        <ListItemButton>
                            <ListItemText primary="Total"/>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                color: totalBalance < 0 ? '#db0000' : 'inherit',
                            }}>
                                <ListItemText
                                    primary={`${currencyFormatter.format(totalBalance)}`}
                                    primaryTypographyProps={{style: {fontWeight: 'bold'}}} // Aplica negrito ao texto
                                />
                            </div>
                        </ListItemButton>
                    </ListItem>
                </List>

                <AccountDialogForm
                    currentAccount={currentAccount}
                    setCurrentAccount={setCurrentAccount}
                    open={openForm}
                    onClose={handleDialogClose}
                    onSave={handleOnSave}
                    onDelete={handleOnDelete}
                />
            </>
        );
    }

export default AccountList;


