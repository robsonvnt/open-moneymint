import {AccountTransaction} from "../models";
import axios, {AxiosResponse} from "axios";
import {format} from "date-fns";


const baseUrl = '/api/finances/transactions'; // ou a URL base do seu backend


export const TransactionService = {

    async getAll(month: Date): Promise<AccountTransaction[]> {
        let monthStr = format(month, 'yyyy-MM');
        let url_call = `${baseUrl}?month=${monthStr}`;
        try {
            const response: AxiosResponse<AccountTransaction[]> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter Categories: ${error}`);
        }
    },

};
