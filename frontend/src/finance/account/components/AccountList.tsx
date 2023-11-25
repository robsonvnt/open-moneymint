import React, {useEffect, useState} from 'react';
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import List from "@mui/material/List";
import {Checkbox, Divider} from "@mui/material";
import {AccountModel} from "../../models";
import {AccountService} from "../AccountService";
import {clearFloatFormatter, currencyFormatter} from "../../../helpers/BRFormatHelper";


const AccountList: React.FC = () => {
    const [checked, setChecked] = React.useState<Map<string, boolean>>(new Map());
    const [accountList, setAccountList] = React.useState<AccountModel[]>([]);
    const accountService = AccountService;
    const [totalBalance, setTotalBalance] = React.useState<number>(0.0);


    const handleToggle = (code: string) => () => {
        let newValue = !checked.get(code);
        const newCheckedMap = new Map(checked.entries());
        newCheckedMap.set(code, newValue);
        setChecked(newCheckedMap);
    };

    useEffect(() => {
        accountService.getAllAccounts()
            .then(accounts => {
                let tmpTotalBalance = 0
                accounts.map(account => {
                    checked.set(account.code, true)
                    tmpTotalBalance += account.balance
                });
                setTotalBalance(tmpTotalBalance)
                setAccountList(accounts);
            });
    }, []);


    return (
        <>
            <center>
                <h4 style={{margin: 15, marginBottom: 2}}>
                    Contas
                </h4>
            </center>
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
                            <ListItemButton>
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
                <Divider light />
                <ListItem disablePadding>
                    <ListItemButton>
                        <ListItemText primary="Total"/>
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            color: totalBalance < 0 ? '#db0000' : 'inherit' // Altera a cor para vermelho se o saldo for negativo
                        }}>
                            <ListItemText
                                primary={`${currencyFormatter.format(totalBalance)}`}
                                primaryTypographyProps={{style: {fontWeight: 'bold'}}} // Aplica negrito ao texto
                            />
                        </div>
                    </ListItemButton>
                </ListItem>
            </List>
        </>
    );
}

export default AccountList;


