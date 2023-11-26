import React, {useState, useEffect} from 'react';
import SideBar from "./components/SideBar";
import Box from '@mui/material/Box';
import MoneyMineAppBar from "../app/MoneyMineAppBar";
import TransactionView from "./transaction/components/TransactionView";


const FinanceHome: React.FC = () => {

    useEffect(() => {

    }, []);

    // SideBar State
    const [accountChecked, setAccountChecked] = React.useState<Map<string, boolean>>(new Map());
    const [selectedCategoryCode, setSelectedCategoryCode] = React.useState<string>("");


    return (
        <Box sx={{display: 'flex'}}>
            <MoneyMineAppBar/>
            <SideBar
                checkedAccounts={accountChecked}
                setCheckedAccounts={setAccountChecked}
                setSelectedCategoryCode={setSelectedCategoryCode}
            />
            <TransactionView
                checkedAccounts={accountChecked}
                selectedCategoryCode={selectedCategoryCode}
            />
        </Box>

    );
}

export default FinanceHome;
