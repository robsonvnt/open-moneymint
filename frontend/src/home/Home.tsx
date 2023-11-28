import React, {useEffect} from 'react';
import MoneyMineAppBar from "../app/MoneyMineAppBar";
import Box from "@mui/material/Box";


const Home: React.FC = () => {

    useEffect(() => {
    }, []);

    return (
        <>
            <Box sx={{display: 'flex'}}>
                <MoneyMineAppBar/>
            </Box>
        </>
    );
};

export default Home;
