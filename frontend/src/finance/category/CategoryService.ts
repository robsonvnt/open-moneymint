import {AccountModel, CategoryModel, CategoryInput, CategoryTreeItem} from "../models";
import axios, {AxiosResponse} from "axios";
import {InputAccountModel} from "../account/components/AccountDialogForm";


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

    async get(categoryCode: string): Promise<CategoryModel> {
        let url_call = `${baseUrl}/${categoryCode}`;
        try {
            const response: AxiosResponse<CategoryModel> = await axios.get(url_call);
            return response.data;
        } catch (error) {
            throw new Error(`Erro ao obter Categories: ${error}`);
        }
    },

    async create(category: CategoryInput): Promise<CategoryModel> {
        const response: AxiosResponse<AccountModel> = await axios.post(baseUrl, category);
        return response.data;
    },

    async update(categoryCode: string, category: CategoryInput): Promise<CategoryModel> {
        let url_call = `${baseUrl}/${categoryCode}`;
        const response: AxiosResponse<AccountModel> = await axios.put(url_call, category);
        return response.data;
    },

    async delete(categoryCode: string): Promise<CategoryModel> {
        let url_call = `${baseUrl}/${categoryCode}`;
        const response: AxiosResponse<AccountModel> = await axios.delete(url_call);
        return response.data;
    },

};
