import React, {useEffect} from 'react';
import {Drawer} from "@mui/material";
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import AccountList from "../account/components/AccountList";
import CategoryTree from "../category/components/CategoryTree";


const SideBar: React.FC = () => {

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
                <AccountList />
                <Divider />
                <List>
                    <CategoryTree/>
                </List>
            </Box>
        </Drawer>
    );
}

export default SideBar;


