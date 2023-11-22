import * as React from 'react';
import { LineChart } from '@mui/x-charts/LineChart';
import InvestmentsService from '../../InvestmentsService';

type AssetAccumulation = {
  portfolio_code: string,
  date: string,
  balance: number,
  amount_invested: number
}

interface AssetAccumulationChart {
  portfolio_code: string;
}

const AssetAccumulationChart: React.FC<AssetAccumulationChart> = ({
  portfolio_code
}) => {

  const [dates, setDates] = React.useState<Date[]>([new Date]);
  const [amountInvested, setAmountInvested] = React.useState<number[]>([1]);
  const [balance, setBalance] = React.useState<number[]>([1]);
  const investmentsService = InvestmentsService;

  const loadAssetAccumulation = () => {
    if (portfolio_code) {
      investmentsService.getAssetAccumulation(portfolio_code)
        .then(assetAccumulation => {
          if (Array.isArray(assetAccumulation)) {

            let items: AssetAccumulation[] = assetAccumulation;

            let loadedDates: Date[] = [];
            let loadedAmountInvested: number[] = [];
            let loadedBalance: number[] = [];

            items.forEach(item => {
              loadedDates.push(new Date(item.date));
              loadedAmountInvested.push(item.amount_invested);
              let diff = item.balance - item.amount_invested;
              loadedBalance.push(diff);
            })

            setDates(loadedDates);
            setAmountInvested(loadedAmountInvested);
            setBalance(loadedBalance);

          }
        });
    }
  }

  React.useEffect(() => {
    loadAssetAccumulation();
  }, [portfolio_code]);

  if (dates.length == 0 || amountInvested.length == 0 || balance.length == 0) {
    return <div>Nenhuma Consolidação encontrada.</div>;
  }

  return (
    <LineChart
      xAxis={[
        {
          id: 'Mês',
          data: dates,
          scaleType: 'time',
          valueFormatter: (date) => {
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const year = date.getFullYear();
            return `${month}/${year}`;
          }
        },
      ]}
      series={[
        {
          id: 'CA',
          label: 'Quantidade Investida',
          data: amountInvested,
          stack: 'total',
          area: true,
          showMark: false,
          stackOffset: "none",
          color: '#4e79a7'
        },
        {
          id: 'R',
          label: 'Rendimento',
          data: balance,
          stack: 'total',
          area: true,
          showMark: false,
          stackOffset: "none",
          color: '#59a14f'
        },
      ]}
      height={300}
    />
  );
}

export default AssetAccumulationChart;

// 'expand' | 'diverging' | 'none' | 'silhouette' | 'wiggle'