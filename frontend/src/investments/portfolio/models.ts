
export interface Portfolio {
  id?: number;
  code?: string;
  name?: string;
  description?: string;
}


export interface PortfolioConsolidationModel {
  code: string,
  name: string,
  description: string,
  amount_invested: number,
  current_balance: number,
  portfolio_yield: number,
}
