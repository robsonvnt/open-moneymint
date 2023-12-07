import {AccountModel} from "../models";
import axios, {AxiosResponse} from "axios";
import {InputAccountModel} from "./components/AccountDialogForm";


const baseUrl = '/api/finances/accounts'; // ou a URL base do seu backend


export const AccountService = {

    async getAllAccounts(): Promise<AccountModel[]> {
        const response: AxiosResponse<AccountModel[]> = await axios.get(baseUrl);
        return response.data;

    },

    async get(code: string): Promise<AccountModel> {
        const response: AxiosResponse<AccountModel> = await axios.get(`${baseUrl}/${code}`);
        return response.data;

    },

    async delete(code: string): Promise<AccountModel> {
        const response: AxiosResponse<AccountModel> = await axios.delete(`${baseUrl}/${code}`);
        return response.data;

    },

    async update(account: InputAccountModel): Promise<AccountModel> {
        const response: AxiosResponse<AccountModel> = await axios.put(`${baseUrl}/${account.code}`, account);
        return response.data;
    },

    async create(account: InputAccountModel): Promise<AccountModel> {
        const response: AxiosResponse<AccountModel> = await axios.post(baseUrl, account);
        return response.data;
    },

};
