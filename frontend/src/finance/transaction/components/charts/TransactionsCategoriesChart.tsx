import * as React from 'react';
import {PieChart, pieArcLabelClasses} from '@mui/x-charts/PieChart';
import {PieItemIdentifier, DefaultizedPieValueType} from '@mui/x-charts/models';
import {AccountConsolidationsService} from "../../../accountConsolidations/AccountConsolidationsService";


type CategoryValueItem = {
    category: string;
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

interface TransactionsCategoriesChartProps {
    accountCodesMap: Map<string, boolean>;
    date: Date
}

const TransactionsCategoriesChart: React.FC<TransactionsCategoriesChartProps> =
    ({
         accountCodesMap, date
     }) => {

        const [categoryValuesItems, setCategoryValuesItems]
            = React.useState<ChatAssetItem[]>([]);
        const [total, setTotal]
            = React.useState<number>(0);

        const [identifier, setIdentifier] = React.useState<null | PieItemIdentifier>(null);
        const [id, setId] = React.useState<undefined | string | number>(undefined);

        const consolidationService = AccountConsolidationsService;


        const loadCategoryValues = () => {
            const accountCodes = Array.from(accountCodesMap.keys()).filter(key => accountCodesMap.get(key) === true);
            if (accountCodes.length === 0)
                return;
            consolidationService.getValuesByCategory(accountCodes, date)
                .then(categoryValues => {
                    if (Array.isArray(categoryValues)) {

                        let items: CategoryValueItem[] = categoryValues;
                        const totalValue = items.reduce((accumulator, currentItem) => {
                            return accumulator + currentItem.value * -1;
                        }, 0);

                        const convertedAssets: ChatAssetItem[] = items.map((asset, index) => ({
                            id: index,
                            label: asset.category,
                            value: asset.value*-1,
                            color: colors[index],
                        }));


                        setTotal(totalValue)
                        setCategoryValuesItems(convertedAssets)

                    }
                });
        }

        React.useEffect(() => {
            loadCategoryValues();
        }, [accountCodesMap, date]);


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
                        data: categoryValuesItems,
                        arcLabel: getArcLabel,
                    },
                ]}
                // width={400}
                height={160}
                sx={{
                    [`& .${pieArcLabelClasses.root}`]: {
                        fill: 'white',
                        fontSize: 14,
                    },
                }}
            />
        );
    }

export default TransactionsCategoriesChart;

