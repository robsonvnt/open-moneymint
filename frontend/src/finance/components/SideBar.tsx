import React, {useEffect} from 'react';
import {Drawer} from "@mui/material";
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Divider from '@mui/material/Divider';
import AccountList from "../account/components/AccountList";
import CategoryTree from "../category/components/CategoryTree";

interface SideBarProps {
    checkedAccounts: Map<string, boolean>;
    setCheckedAccounts: React.Dispatch<React.SetStateAction<Map<string, boolean>>>;
    selectedCategoryCode: string;
}

const SideBar: React.FC<SideBarProps> =
    ({
         checkedAccounts,
         setCheckedAccounts,
         selectedCategoryCode
     }) => {

        useEffect(() => {

        }, []);


        return (
            <Drawer
                variant="permanent"
                sx={{
                    width: 240,
                    flexShrink: 0,
                    [`& .MuiDrawer-paper`]: {width: 240, boxSizing: 'border-box'},
                }}
            >
                <Toolbar/>
                <Box sx={{overflow: 'auto'}}>
                    <AccountList
                        checked={checkedAccounts}
                        setChecked={setCheckedAccounts}
                    />
                    <Divider/>
                    <CategoryTree
                        selectedCategoryCode={selectedCategoryCode}
                    />

                </Box>
            </Drawer>
        );
    }

export default SideBar;


