import {AccountTransaction} from "../models";
import axios, {AxiosResponse} from "axios";


const baseUrl = '/api/finances/transactions'; // ou a URL base do seu backend


export const TransactionService = {

    async getAll(): Promise<AccountTransaction[]> {
        let url_call = `${baseUrl}`;
        try {
            const response: AxiosResponse<AccountTransaction[]> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter Categories: ${error}`);
        }
    },

};
