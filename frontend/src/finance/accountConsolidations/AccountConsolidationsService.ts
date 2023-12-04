import {AccountConsolidationModel} from "../models";
import axios, {AxiosResponse} from "axios";
import {formatDate, formatMonth} from "../../helpers/BRFormatHelper";


const baseUrl = '/api/finances/consolidations'; // ou a URL base do seu backend


export const AccountConsolidationsService = {

    async getConsolidation(accountCodes: string[], date: Date): Promise<AccountConsolidationModel[]> {
        let month = formatMonth(date)
        let codesStr = '';
        accountCodes.map(code => codesStr += `&account_codes=${code}`)
        const urlCall = `${baseUrl}?month=${month}&${codesStr}`;
        const response: AxiosResponse<AccountConsolidationModel[]> =
            await axios.get(urlCall);
        return response.data;

    },

};
