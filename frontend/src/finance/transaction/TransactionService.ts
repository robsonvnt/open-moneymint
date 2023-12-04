import {AccountTransaction, InputAccountTransaction} from "../models";
import axios, {AxiosResponse} from "axios";
import {format} from "date-fns";


const baseUrl = '/api/finances/transactions'; // ou a URL base do seu backend


export const TransactionService = {

    async getAll(
        month: Date, accountCodes: string[], selectedCategoryCodes: string[]
    ): Promise<AccountTransaction[]> {
        let monthStr = format(month, 'yyyy-MM');
        let url_call = `${baseUrl}?month=${monthStr}`;
        accountCodes.map(code => url_call += `&account_codes=${code}`)
        selectedCategoryCodes.map(code => url_call += `&category_codes=${code}`)
        try {
            const response: AxiosResponse<AccountTransaction[]> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter Categories: ${error}`);
        }
    },

    async create(transaction: InputAccountTransaction): Promise<AccountTransaction> {
        let url_call = `${baseUrl}`;
        const response: AxiosResponse<AccountTransaction> = await axios.post(url_call, transaction);
        return response.data;
    },

    async update(transaction: InputAccountTransaction): Promise<AccountTransaction> {
        let url_call = `${baseUrl}/${transaction.code}`;
        const response: AxiosResponse<AccountTransaction> = await axios.put(url_call, transaction);
        return response.data;
    },

    async delete(code: string): Promise<void> {
        let url_call = `${baseUrl}/${code}`;
        return await axios.delete(url_call);
    },

    async get(code: string): Promise<AccountTransaction> {
        let url_call = `${baseUrl}/${code}`;
        const response: AxiosResponse<AccountTransaction> = await axios.get(url_call);
        return response.data;
    }

};
