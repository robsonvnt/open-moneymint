import * as React from 'react';
import { PieChart, pieArcLabelClasses } from '@mui/x-charts/PieChart';
import { PieItemIdentifier, DefaultizedPieValueType } from '@mui/x-charts/models';
import InvestmentsService from '../../InvestmentsService';
import { getAssetTypeLabel } from '../../models';


type DiversificationItem = {
    asset_type: string;
    value: number;
}

type ChatAssetItem = {
    id: number;
    label: string;
    value: number;
};

let colors = [
    '#4e79a7', // Azul
    '#f28e2c', // Laranja
    '#e15759', // Vermelho
    '#76b7b2', // Turquesa
    '#59a14f', // Verde
    '#edc949', // Amarelo
    '#af7aa1', // Roxo
    '#ff9da7', // Rosa
    '#9c755f', // Marrom
    '#bab0ab', // Bege
]

interface InvestmentDiversificationChartI {
    portfolio_code: string;
    reloadChart: boolean;
}

const InvestmentDiversificationChart: React.FC<InvestmentDiversificationChartI> = ({
    portfolio_code, reloadChart
}) => {

    const [portfolioDiversificationItems, setPortfolioDiversificationItems]
        = React.useState<ChatAssetItem[]>([]);
    const [total, setTotal]
        = React.useState<number>(0);

    const [identifier, setIdentifier] = React.useState<null | PieItemIdentifier>(null);
    const [id, setId] = React.useState<undefined | string | number>(undefined);

    const investmentsService = InvestmentsService;



    const loadDiversification = () => {
        if (portfolio_code) {
            investmentsService.getDiversificationPortfolio(portfolio_code)
                .then(diversification => {
                    if (Array.isArray(diversification)) {

                        let items: DiversificationItem[] = diversification;
                        const totalValue = items.reduce((accumulator, currentItem) => {
                            return accumulator + currentItem.value;
                        }, 0);

                        const convertedAssets: ChatAssetItem[] = items.map((asset, index) => ({
                            id: index,
                            label: getAssetTypeLabel(asset.asset_type),
                            value: asset.value,
                            color: colors[index],
                        }));


                        setTotal(totalValue)
                        setPortfolioDiversificationItems(convertedAssets)
                    }
                });
        }
    }

    React.useEffect(() => {
        loadDiversification();
    }, [portfolio_code, reloadChart]);


    const handleClick = (
        event: React.MouseEvent<SVGPathElement, MouseEvent>,
        itemIdentifier: PieItemIdentifier,
        item: DefaultizedPieValueType,
    ) => {
        setId(item.id);
        setIdentifier(itemIdentifier);
    };


    const getArcLabel = (params: DefaultizedPieValueType) => {
        const percent = params.value / total;
        return `${(percent * 100).toFixed(0)}%`;
    };

    return (
        <PieChart
            series={[
                {
                    data: portfolioDiversificationItems,
                    arcLabel: getArcLabel,
                },
            ]}
            onClick={handleClick}
            height={300}
            margin={{ right: 200 }}
            sx={{
                [`& .${pieArcLabelClasses.root}`]: {
                    fill: 'white',
                    fontSize: 14,
                },
            }}
        />
    );
}

export default InvestmentDiversificationChart;

