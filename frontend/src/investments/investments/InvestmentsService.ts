// InvestmentService.ts

import axios from "axios";
import { Investment } from "./models";

export interface ErrorResponse {
  error: string;
}

class InvestmentService {

  async createInvestment(portfolio_code: string, investment: Investment): Promise<Investment | ErrorResponse> {
    try {
      const response = await axios.post<Investment>(`/api/portfolios/${portfolio_code}/investments`, investment);
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

  async updateInvestment(portfolio_code: string, investment_code: string, investment: Investment): Promise<Investment | ErrorResponse> {
    try {
      const response = await axios.put<Investment>(`/api/portfolios/${portfolio_code}/investments/${investment_code}`, investment);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        // O servidor respondeu com um status fora do intervalo de 2xx
        console.error('Error alterar the investment:', error.response.data);
        return { error: error.response.data.error || 'Unexpected error' };
      } else {
        // Alguma coisa aconteceu na configuração da solicitação e desencadeou um erro
        console.error('Error alterar the investment:', error.message);
        return { error: error.message };
      }
    }
  }

  async updateAllInvestmentStockPrice(portfolio_code: string) {
    await axios.put<Investment>(`/api/portfolios/${portfolio_code}/investments-prices/`);
    await axios.post<Investment>(`/api/portfolios/${portfolio_code}/consolidations/consolidate/`);
  }

  async deleteInvestment(portfolio_code: string, investment_code: string): Promise<Investment | ErrorResponse> {
    try {
      const response = await axios.delete<Investment>(`/api/portfolios/${portfolio_code}/investments/${investment_code}`);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        // O servidor respondeu com um status fora do intervalo de 2xx
        console.error('Error deletar the investment:', error.response.data);
        return { error: error.response.data.error || 'Unexpected error' };
      } else {
        // Alguma coisa aconteceu na configuração da solicitação e desencadeou um erro
        console.error('Error deletar the investment:', error.message);
        return { error: error.message };
      }
    }
  }

  async filterByPortifolio(portfolio_code: string): Promise<Investment[] | ErrorResponse> {
    try {
      const response = await axios.get<Investment[]>(`/api/portfolios/${portfolio_code}/investments/`);

      let investments = response.data;

      // Ordenando os investimentos por (current_average_price - purchase_price)
      investments = investments.sort((a, b) => {
        // Calculando a diferença para cada investimento
        const diffA = (a.current_average_price ?? 0) - a.purchase_price;
        const diffB = (b.current_average_price ?? 0) - b.purchase_price;

        // Ordenando em ordem decrescente (para ordem crescente, inverta a e b)
        return diffB - diffA;
      });
      return investments;

    } catch (error: any) {
      if (error.response) {
        console.error('Error fetching investments:', error.response.data);
        return { error: error.response.data.error || 'Unexpected error' };
      } else {
        console.error('Error fetching investments:', error.message);
        return { error: error.message };
      }
    }
  }

  async getDiversificationPortfolio(portfolio_code: string): Promise<[] | ErrorResponse> {
    try {
      const response = await axios.get<[]>(`/api/portfolios/${portfolio_code}/investments-diversification/`);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        console.error('Error fetching investments:', error.response.data);
        return { error: error.response.data.error || 'Unexpected error' };
      } else {
        console.error('Error fetching investments:', error.message);
        return { error: error.message };
      }
    }
  }

  async getAssetAccumulation(portfolio_code: string): Promise<[] | ErrorResponse> {
    try {
      const response = await axios.get<[]>(`/api/portfolios/${portfolio_code}/consolidations/`);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        console.error('Error fetching investments:', error.response.data);
        return { error: error.response.data.error || 'Unexpected error' };
      } else {
        console.error('Error fetching investments:', error.message);
        return { error: error.message };
      }
    }
  }

  // Adicione métodos semelhantes para updateInvestment, deleteInvestment, e qualquer outra operação que você precise.
}

export default new InvestmentService();
