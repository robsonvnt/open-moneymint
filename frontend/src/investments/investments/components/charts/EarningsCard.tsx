import React from 'react';
import { Card, CardContent, Typography, IconButton } from '@mui/material';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';

interface EarningsCardProps {
    amount: string;
    label: string;
    valueIncreased: boolean;
    percentageChange?: number;
}

const red_color = '#e15759';
const green_color = '#59a14f';

const EarningsCard: React.FC<EarningsCardProps> = ({
    amount, label, valueIncreased, percentageChange
}) => {

    return (
        <Card style={{
            // backgroundColor: '#6c5ce7',
            // color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '16px',
            width: '100%',
            minHeight: 150
        }}>
            <IconButton color="inherit">
                <AttachMoneyIcon fontSize="large" />
            </IconButton>
            <CardContent>
                <div style={{ display: 'flex', alignItems: 'center' }}>
                    <Typography
                        variant="h4"
                        component="div"
                        style={{ color: valueIncreased ? green_color : red_color }}
                    >
                        {amount}
                    </Typography>

                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        marginLeft: 10
                    }}>
                        {/* Ícone de acordo com a condição */}
                        {valueIncreased ?
                            <ArrowDropUpIcon style={{ color: green_color, fontSize: '2rem' }} /> :
                            <ArrowDropDownIcon style={{ color: red_color, fontSize: '2rem' }} />
                        }
                        {percentageChange !== undefined &&
                            <Typography
                                component="div"
                                style={{
                                    color: valueIncreased ? green_color : red_color,
                                }}
                            >

                                {Math.round(percentageChange * 10) / 10}%
                            </Typography>
                        }
                    </div>

                </div>
                <Typography variant="subtitle1" component="div">
                    {label}
                </Typography>
            </CardContent>
            <IconButton color="inherit">
                <MoreVertIcon />
            </IconButton>
        </Card>
    );
};

export default EarningsCard;
