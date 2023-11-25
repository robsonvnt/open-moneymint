import React, {useState, useEffect} from 'react';
import SideBar from "./components/SideBar";
import Box from '@mui/material/Box';
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import {Typography} from "@mui/material";
import MoneyMineAppBar from "../app/MoneyMineAppBar";
import TransactionView from "./transaction/components/TransactionView";


const FinanceHome: React.FC = () => {

    useEffect(() => {

    }, []);


    return (
        <Box sx={{display: 'flex'}}>
            <MoneyMineAppBar/>
            <SideBar/>
            <TransactionView/>
        </Box>

    );
}

export default FinanceHome;
