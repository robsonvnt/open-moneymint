import {AccountModel} from "../models";
import axios, {AxiosResponse} from "axios";


const baseUrl = '/api/finances/accounts'; // ou a URL base do seu backend


export const AccountService = {

    async getAllAccounts(): Promise<AccountModel[]> {
        let url_call = `${baseUrl}`;
        try {
            const response: AxiosResponse<AccountModel[]> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter accounts: ${error}`);
        }
    },

};
