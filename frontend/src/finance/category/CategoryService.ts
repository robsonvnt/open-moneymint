import {AccountModel, CategoryModel, CategoryTreeItem} from "../models";
import axios, {AxiosResponse} from "axios";
import {NewAccountModel} from "../account/components/AccountDialogForm";
import {NewCategoryModel} from "./components/CategoryDialogForm";


const baseUrl = '/api/finances/categories'; // ou a URL base do seu backend


export const CategoryService = {

    async getAllCategories(): Promise<CategoryTreeItem[]> {
        let url_call = `${baseUrl}`;
        try {
            const response: AxiosResponse<CategoryTreeItem[]> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter Categories: ${error}`);
        }
    },

    async getAllCategoriesList(): Promise<CategoryTreeItem[]> {
        let url_call = `${baseUrl}/list`;
        try {
            const response: AxiosResponse<CategoryTreeItem[]> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter Categories: ${error}`);
        }
    },

    async create(account: NewCategoryModel): Promise<CategoryModel> {
        const response: AxiosResponse<AccountModel> = await axios.post(baseUrl, account);
        return response.data;
    },

};
