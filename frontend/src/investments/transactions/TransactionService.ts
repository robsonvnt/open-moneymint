
import axios, { AxiosResponse } from 'axios';
import { TransactionModel, NewTransaction } from './models';

const baseUrl = '/api/portfolios'; // ou a URL base do seu backend

export interface ErrorResponse {
  error: string;
}

const fetchOptions = {
  headers: {
    'Content-Type': 'application/json',
  },
};

export const TransactionService = {
  async getAllTransactions(portfolioCode: string, investmentCode: string): Promise<TransactionModel[]> {
    let url_call = `${baseUrl}/${portfolioCode}/investments/${investmentCode}/transactions`;
    try {
      const response: AxiosResponse<TransactionModel[]> = await axios.get(url_call);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter portfólios: ${error}`);
    }
  },

  async delete(portfolioCode: string, investmentCode: string, transactionCode: string): Promise<void> {
    try {
      let url_call = `${baseUrl}/${portfolioCode}/investments/${investmentCode}/transactions/${transactionCode}`;
      await axios.delete(url_call);
    } catch (error) {
      throw new Error(`Erro ao deletar o portfólio: ${error}`);
    }
  },

  async getTransaction(portfolioCode: string, investmentCode: string, transactionCode: string): Promise<TransactionModel> {
    const response = await fetch(`${baseUrl}/${portfolioCode}/investments/${investmentCode}/transactions/${transactionCode}`, fetchOptions);
    if (!response.ok) {
      throw new Error('Erro ao buscar a transação');
    }
    return response.json();
  },

  async create(portfolioCode: string, investmentCode: string, transaction: NewTransaction): Promise<TransactionModel | ErrorResponse> {
    try {
      let url = `/api/portfolios/${portfolioCode}/investments/${investmentCode}/transactions`
      const response = await axios.post<TransactionModel>(url, transaction);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        // O servidor respondeu com um status fora do intervalo de 2xx
        console.error('Error creating the investment:', error.response.data);
        return { error: error.response.data.error || 'Unexpected error' };
      } else {
        // Alguma coisa aconteceu na configuração da solicitação e desencadeou um erro
        console.error('Error creating the investment:', error.message);
        return { error: error.message };
      }
    }
  }

};
