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
    },

    async uploadTransactionsFile(account_code: string, file: File) {
        let url_call = `${baseUrl}/upload?account_code=${account_code}`;

        const reader = new FileReader();

        reader.onload = function(event) {
            const fileContent = event.target?.result as string;
            const lineCount = (fileContent.match(/\n/g) || []).length + 1; // +1 para incluir a última linha
            console.log(`lineCount: ${lineCount}`)
        };

        reader.onloadend = async () => {
            // Converte o arquivo para base64
            const base64File = reader.result;

            // Prepara o objeto JSON para enviar
            const jsonData = {
                file: base64File,
                filename: file.name,
            };

            try {
                const response = await axios.post(url_call, jsonData);

                console.log('Resultado do upload:', response.data);
                alert('Arquivo enviado com sucesso!');
                return true;
            } catch (error) {
                console.error('Erro ao enviar o arquivo:', error);
                alert('Erro ao enviar arquivo.');
                return false;
            }

        };

        reader.readAsDataURL(file);

        // try {
        //     // Use o Axios para enviar o arquivo
        //     const response = await axios.post(url_call, formData);
        //
        //     console.log('Resultado do upload:', response.data);
        //     alert('Arquivo enviado com sucesso!');
        //     return true;
        // } catch (error) {
        //     console.error('Erro ao enviar o arquivo:', error);
        //     alert('Erro ao enviar arquivo.');
        //     return false;
        // }

    },

};
