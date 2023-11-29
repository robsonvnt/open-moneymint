import React, {useEffect, useState} from 'react';
import MoneyMineAppBar from "../app/MoneyMineAppBar";
import Box from "@mui/material/Box";


const Home: React.FC = () => {

    useEffect(() => {
    }, []);

    // Barra lateral
    const [mobileOpen, setMobileOpen] = useState(false);
    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    return (
        <>
            <Box sx={{display: 'flex'}}>
                <MoneyMineAppBar
                    handleDrawerToggle={handleDrawerToggle}
                />
            </Box>
        </>
    );
};

export default Home;
