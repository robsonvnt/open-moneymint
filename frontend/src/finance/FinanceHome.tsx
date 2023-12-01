import React, {useState, useEffect} from 'react';
import Box from '@mui/material/Box';
import TransactionView from "./transaction/TransactionView";
import {AppBar, Drawer, Grid, IconButton, useMediaQuery, useTheme} from "@mui/material";
import CategoryTree from "./category/components/CategoryTree";
import AccountList from "./account/components/AccountList";
import Divider from "@mui/material/Divider";
import MoneyMineAppBar from "../app/MoneyMineAppBar";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

const drawerWidth = 240;

const FinanceHome: React.FC = () => {

    useEffect(() => {

    }, []);

    const [checkedAccounts, setCheckedAccounts] = React.useState<Map<string, boolean>>(new Map());
    const [selectedCategoryCode, setSelectedCategoryCode] = React.useState<string>("");
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    const [refreshAccounts, setRefreshAccounts] = React.useState<boolean>(false);

    const runRefreshAccounts = () => {
        setRefreshAccounts(true);
        console.log("setRefreshAccounts(true);")
    }

    // Barra lateral
    const [mobileOpen, setMobileOpen] = useState(false);
    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };


    return (
        <Box sx={{display: 'flex'}}>
            <MoneyMineAppBar
                handleDrawerToggle={handleDrawerToggle}
            />


            {!mobileOpen && isMobile && (
                <IconButton
                    onClick={handleDrawerToggle}
                    sx={{
                        position: 'fixed',
                        left: 5,
                        top: 60,
                        zIndex: theme.zIndex.drawer + 1,
                        backgroundColor: 'rgba(0, 0, 0, 0.1)', // Cor de fundo leve
                        borderRadius: '50%', // Faz o botão circular
                        '&:hover': {
                            backgroundColor: 'rgba(0, 0, 0, 0.2)', // Cor de fundo mais escura ao passar o mouse
                        },
                    }}
                >
                    <ChevronRightIcon/>
                </IconButton>
            )}


            {/*Barra lateral*/}
            <Drawer
                variant={isMobile ? 'temporary' : 'permanent'}
                open={mobileOpen}
                onClose={handleDrawerToggle}
                ModalProps={{
                    keepMounted: true, // Melhora a performance em dispositivos móveis
                }}
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    [`& .MuiDrawer-paper`]: {width: drawerWidth, boxSizing: 'border-box'},
                }}
            >
                <div
                    style={{
                        paddingTop: 70
                    }}
                >
                    <AccountList
                        checked={checkedAccounts}
                        setChecked={setCheckedAccounts}
                        refresh={refreshAccounts}
                        setRefresh={setRefreshAccounts}
                    />
                    <Divider/>
                    <CategoryTree
                        selectedCategoryCode={selectedCategoryCode}
                        setSelectedCategoryCode={setSelectedCategoryCode}
                    />
                </div>
            </Drawer>

            {/*Conteúdo*/}
            <Box
                component="main"
                sx={{flexGrow: 1, p: 3, width: {sm: `calc(100% - ${drawerWidth}px)`}}}
                style={{
                    padding: 0, paddingTop: 60
                }}
            >

                <TransactionView
                    checkedAccounts={checkedAccounts}
                    selectedCategoryCode={selectedCategoryCode}
                    reloadAccounts={runRefreshAccounts}
                />

            </Box>
        </Box>
    );
}

export default FinanceHome;
