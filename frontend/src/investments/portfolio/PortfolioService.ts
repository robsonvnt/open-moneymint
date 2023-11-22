// PortfolioService.ts
import axios, { AxiosResponse } from 'axios';
import { Portfolio, PortfolioConsolidationModel } from './models';

class PortfolioService {
  // URL base da API de portfólios
  baseURL: string = '/api/portfolios';

  // Método para obter todos os portfólios
  public async getAll(): Promise<Portfolio[]> {
    try {
      const response: AxiosResponse<Portfolio[]> = await axios.get(this.baseURL);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter portfólios: ${error}`);
    }
  }


  // Método para obter um portfólio por ID
  public async getByCode(code: string): Promise<Portfolio> {
    try {
      const response: AxiosResponse<Portfolio> = await axios.get(`${this.baseURL}/${code}`);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter o portfólio: ${error}`);
    }
  }

  public async getConsolidatedByCode(code: string): Promise<PortfolioConsolidationModel> {
    try {
      const response: AxiosResponse<PortfolioConsolidationModel> = await axios.get(`${this.baseURL}/portfolio-consolidation/${code}`);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao obter o portfólio: ${error}`);
    }
  }

  // Método para criar um novo portfólio
  public async create(portfolio: Portfolio): Promise<Portfolio> {
    try {
      const response: AxiosResponse<Portfolio> = await axios.post(this.baseURL, portfolio);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao criar o portfólio: ${error}`);
    }
  }

  // Método para atualizar um portfólio
  public async update(code: string, portfolio: Portfolio): Promise<Portfolio> {
    try {
      const response: AxiosResponse<Portfolio> = await axios.put(`${this.baseURL}/${code}`, portfolio);
      return response.data;
    } catch (error) {
      throw new Error(`Erro ao atualizar o portfólio: ${error}`);
    }
  }

  // Método para deletar um portfólio
  public async delete(code: string): Promise<void> {
    try {
      await axios.delete(`${this.baseURL}/${code}`);
    } catch (error) {
      throw new Error(`Erro ao deletar o portfólio: ${error}`);
    }
  }
}

export default new PortfolioService(); // Exportando uma instância da classe
