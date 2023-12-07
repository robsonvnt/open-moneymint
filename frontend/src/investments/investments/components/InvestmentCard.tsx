// InvestmentCard.tsx
import * as React from 'react';
import { CardContent, Typography } from '@mui/material';
import { AssetType, Investment, getAssetTypeLabel } from '../models';
import { currencyFormatter, formatDateStr } from '../../../helpers/BRFormatHelper';

interface InvestmentCardProps {
    investment: Investment;
    onClick: (investment: Investment) => void;
}

const InvestmentCard: React.FC<InvestmentCardProps> = ({ investment, onClick }) => {
    const {
        ticker,
        asset_type,
        purchase_date,
        quantity,
        purchase_price,
        current_average_price,
    } = investment;

    let percentageChange = 0;
    let balance = 0;
    if (current_average_price) {
        percentageChange = ((current_average_price - purchase_price) / purchase_price) * 100;
        balance = quantity * current_average_price;
    }

    const percentageColor = percentageChange >= 0 ? 'green' : 'red';

    return (
        <CardContent
            onClick={() => onClick(investment)}
        >
            <Typography gutterBottom variant="h5" component="div">
                {ticker}
            </Typography>
            <Typography variant="body2" color="text.secondary">
                <b>{getAssetTypeLabel(asset_type)}</b>
            </Typography>

            <Typography variant="body2" color="text.secondary">
                {formatDateStr(purchase_date)}
            </Typography>
            {asset_type !== AssetType.FIXED_INCOME && asset_type !== AssetType.PRIVATE_EQUITY_FUND && (
                <Typography variant="body2" color="text.primary">
                    Quantidade: <b>{quantity}</b>
                </Typography>
            )}
            <Typography variant="body2" color="text.primary">
                {asset_type === AssetType.FIXED_INCOME || asset_type === AssetType.PRIVATE_EQUITY_FUND ?
                    "Valor Aplicado: " : "Preço Médio (compra): "}
                <b>{currencyFormatter.format(purchase_price)}</b>
            </Typography>
            <Typography variant="body2" color="text.primary">
                {asset_type === AssetType.FIXED_INCOME || asset_type === AssetType.PRIVATE_EQUITY_FUND ?
                    "Saldo Atual: " : "Preço Atual: "}
                <b>{currencyFormatter.format(current_average_price ? current_average_price : 0.0)}</b>
            </Typography>
            <Typography variant="body2" style={{ color: percentageColor }}>
                {asset_type === AssetType.FIXED_INCOME || asset_type === AssetType.PRIVATE_EQUITY_FUND ?
                    "Rendimento: " : "Variação: "}
                <b>{percentageChange.toFixed(2)}%</b>
            </Typography>
            <Typography variant="body2" color="text.primary">
                Saldo Atual: <b>{currencyFormatter.format(balance)}</b>
            </Typography>
        </CardContent>
    );
}

export default InvestmentCard;
