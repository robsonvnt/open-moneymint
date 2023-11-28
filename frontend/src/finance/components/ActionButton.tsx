import React, {useState} from 'react';
import Fab from '@mui/material/Fab';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import AddIcon from '@mui/icons-material/Add';

const ActionButton: React.FC = () => {
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    // Substitua essas funções pelas ações reais
    const handleAction1 = () => {
        console.log("Ação 1");
        handleClose();
    };

    const handleAction2 = () => {
        console.log("Ação 2");
        handleClose();
    };

    const handleAction3 = () => {
        console.log("Ação 3");
        handleClose();
    };

    return (
        <div>
            <Fab color="primary" aria-label="add" onClick={handleClick}
                 style={{position: 'fixed', bottom: '20px', right: '20px'}}>
                <AddIcon/>
            </Fab>
            <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={handleAction1}>Ação 1</MenuItem>
                <MenuItem onClick={handleAction2}>Ação 2</MenuItem>
                <MenuItem onClick={handleAction3}>Ação 3</MenuItem>
            </Menu>
        </div>
    );
};

export default ActionButton;
