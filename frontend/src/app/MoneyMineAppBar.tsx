import * as React from 'react';
import {styled} from '@mui/material/styles';
import MuiAppBar, {AppBarProps as MuiAppBarProps} from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import SavingsIcon from '@mui/icons-material/Savings';
import Typography from '@mui/material/Typography';
import MenuIcon from '@mui/icons-material/Menu';
import {useNavigate} from "react-router-dom";
import {AppBar, Avatar, Box, Button, Tooltip, useMediaQuery, useTheme} from "@mui/material";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";

interface MoneyMineAppBarProps {
    handleDrawerToggle: () => void;
}

const MoneyMineAppBar: React.FC<MoneyMineAppBarProps> =
    ({
         handleDrawerToggle
     }) => {

        const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
        const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);
        const navigate = useNavigate();
        const theme = useTheme();
        const isMobile = useMediaQuery(theme.breakpoints.down('md'));


        const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
            setAnchorElNav(event.currentTarget);
        };
        const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
            setAnchorElUser(event.currentTarget);
        };

        const handleCloseNavMenu = () => {
            setAnchorElNav(null);
        };

        const handleCloseUserMenu = () => {
            setAnchorElUser(null);
        };

        interface AppBarProps extends MuiAppBarProps {
            open?: boolean;
        }

        const drawerWidth: number = 240;

        const AppBar = styled(MuiAppBar, {
            shouldForwardProp: (prop) => prop !== 'open',
        })<AppBarProps>(({theme, open}) => ({
            zIndex: theme.zIndex.drawer + 1,
            transition: theme.transitions.create(['width', 'margin'], {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.leavingScreen,
            }),
            ...(open && {
                marginLeft: drawerWidth,
                width: `calc(100% - ${drawerWidth}px)`,
                transition: theme.transitions.create(['width', 'margin'], {
                    easing: theme.transitions.easing.sharp,
                    duration: theme.transitions.duration.enteringScreen,
                }),
            }),
        }));

        return (

            <AppBar  sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
                <Toolbar>
                    {isMobile && (
                        <IconButton
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            onClick={handleOpenNavMenu}
                            sx={{mr: 2}}
                        >
                            <MenuIcon/>
                        </IconButton>
                    )}
                    <SavingsIcon sx={{
                        // display: {xs: 'none', md: 'flex'},
                        mr: 1
                    }}/>

                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        href="#app-bar-with-responsive-menu"
                        sx={{
                            mr: 2,
                            // display: {xs: 'none', md: 'flex'},
                            fontFamily: 'monospace',
                            fontWeight: 700,
                            letterSpacing: '.3rem',
                            color: 'inherit',
                            textDecoration: 'none',
                        }}
                    >
                        MoneyMint
                    </Typography>


                    <Box sx={{flexGrow: 1, display: {xs: 'none', md: 'flex'}}}>
                        <Button
                            onClick={() => {
                                navigate('/finances');
                            }}
                            sx={{my: 2, color: 'white', display: 'block'}}
                        >
                            Finanças
                        </Button>
                        <Button
                            onClick={() => {
                                navigate('/investments');
                            }}
                            sx={{my: 2, color: 'white', display: 'block'}}
                        >
                            Investimentos
                        </Button>
                    </Box>


                    <Box sx={{flexGrow: 1, display: {xs: 'flex', md: 'none'}}}>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'left',
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{
                                display: {xs: 'block', md: 'none'},
                            }}
                            style={{
                                marginTop: 40
                            }}
                        >
                            <MenuItem onClick={() => {
                                navigate('/finances');
                                setAnchorElNav(null);
                            }}>
                                <Typography textAlign="center">Finanças</Typography>
                            </MenuItem>

                            <MenuItem onClick={() => {
                                navigate('/investments');
                                setAnchorElNav(null);
                            }}>
                                <Typography textAlign="center">Investimentos</Typography>
                            </MenuItem>

                        </Menu>
                    </Box>

                    <Box sx={{flexGrow: 0}}>
                        <Tooltip title="Open settings">
                            <IconButton onClick={handleOpenUserMenu} sx={{p: 0}}>
                                <Avatar alt="Remy Sharp" src="/static/images/avatar/2.jpg"/>
                            </IconButton>
                        </Tooltip>
                        <Menu
                            sx={{mt: '45px'}}
                            id="menu-appbar"
                            anchorEl={anchorElUser}
                            anchorOrigin={{
                                vertical: 'bottom', // Ajuste para 'bottom'
                                horizontal: 'right',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top', // Ajuste para 'top'
                                horizontal: 'right',
                            }}
                            open={Boolean(anchorElUser)}
                            onClose={handleCloseUserMenu}
                        >

                            <MenuItem key="profile">
                                <Typography textAlign="center">Account</Typography>
                            </MenuItem>
                            <MenuItem key="profile">
                                <Typography textAlign="center"
                                            onClick={() => {
                                                localStorage.removeItem('accessToken');
                                                navigate('/login');
                                            }}
                                >Logout</Typography>
                            </MenuItem>


                        </Menu>
                    </Box>


                </Toolbar>
            </AppBar>


            // <AppBar position="fixed" sx={{zIndex: (theme) => theme.zIndex.drawer + 1}}>
            //     <Container maxWidth="xl">
            //         <Toolbar >
            //             <SavingsIcon sx={{display: {xs: 'none', md: 'flex'}, mr: 1}}/>
            //
            //

            //             <SavingsIcon sx={{display: {xs: 'flex', md: 'none'}, mr: 1}}/>
            //             <Typography
            //                 variant="h5"
            //                 noWrap
            //                 component="a"
            //                 href="#app-bar-with-responsive-menu"
            //                 sx={{
            //                     mr: 2,
            //                     display: {xs: 'flex', md: 'none'},
            //                     flexGrow: 1,
            //                     fontFamily: 'monospace',
            //                     fontWeight: 700,
            //                     letterSpacing: '.3rem',
            //                     color: 'inherit',
            //                     textDecoration: 'none',
            //                 }}
            //             >
            //                 MoneyMint
            //             </Typography>

            //

            //         </Toolbar>
            //     </Container>
            // </AppBar>
        )
            ;
    }

export default MoneyMineAppBar;