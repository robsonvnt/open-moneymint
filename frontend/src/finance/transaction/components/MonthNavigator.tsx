import React from 'react';
import {addMonths, format, subMonths} from 'date-fns';
import {ptBR} from 'date-fns/locale';
import IconButton from '@mui/material/IconButton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

interface MonthNavigatorProps {
    currentDate: Date;
    setCurrentDate: (date: Date) => void;
}

const MonthNavigator: React.FC<MonthNavigatorProps> = (
    {
        currentDate,
        setCurrentDate,
    }) => {

    const capitalize = (str: string) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    };

    const handlePreviousMonth = () => {
        setCurrentDate(subMonths(currentDate, 1));
    };

    const handleNextMonth = () => {
        setCurrentDate(addMonths(currentDate, 1));
    };

    return (
        <div style={{display: 'flex', alignItems: 'center'}}>
            <IconButton onClick={handlePreviousMonth}>
                <ArrowBackIcon/>
            </IconButton>
            <div style={{minWidth: '220px', textAlign: 'center'}}>
                <span><b>{capitalize(format(currentDate, "MMMM 'de' yyyy", {locale: ptBR}))}</b></span>
            </div>

            <IconButton onClick={handleNextMonth}>
                <ArrowForwardIcon/>
            </IconButton>
        </div>
    );
};

export default MonthNavigator;
