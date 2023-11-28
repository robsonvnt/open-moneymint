import {AccountModel} from "../models";
import axios, {AxiosResponse} from "axios";
import {NewAccountModel} from "./components/AccountDialogForm";


const baseUrl = '/api/finances/accounts'; // ou a URL base do seu backend


export const AccountService = {

    async getAllAccounts(): Promise<AccountModel[]> {
        const response: AxiosResponse<AccountModel[]> = await axios.get(baseUrl);
        return response.data;

    },

    async create(account: NewAccountModel): Promise<AccountModel> {
        const response: AxiosResponse<AccountModel> = await axios.post(baseUrl, account);
        return response.data;
    },

};
