import {AccountModel, CategoryModel, CategoryTreeItem} from "../models";
import axios, {AxiosResponse} from "axios";


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

};
