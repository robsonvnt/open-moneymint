
export interface NewTransaction {
  investment_code: string;
  type: string;
  date: string;
  quantity: number;
  price: number;
}


export interface TransactionModel {
  code: string,
  investment_code: string;
  type: string;
  date: string;
  quantity: number;
  price: number;
}
