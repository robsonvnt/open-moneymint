export interface Investment {
    code?: string;
    portfolio_code: string;
    asset_type: string;
    ticker: string;
    quantity: number;
    purchase_price: number;
    purchase_date: string;
    current_average_price?: number;
}

export const createEmptynvestment = (): Investment => {
    return {
        portfolio_code: "",
        asset_type: "",
        ticker: "",
        quantity: 0,
        purchase_price: 0,
        purchase_date: "",
        current_average_price: 0
    }
}

export enum AssetType {
    STOCK = "STOCK",
    REIT = "REIT",
    FIXED_INCOME = "FIXED_INCOME",
    PRIVATE_EQUITY_FUND = "PRIVATE_EQUITY_FUND"
}

export const getAssetTypeLabel = (key: string): string => {
    let values: { [key: string]: string | undefined } = {
        "STOCK": "Ações",
        "REIT": "FII",
        "FIXED_INCOME": "Renda Fixa",
        "PRIVATE_EQUITY_FUND": "Fundos Privados"
    };
    const label = values[key];
    if (typeof label === 'undefined') {
        throw new Error(`Label for key "${key}" not found.`);
    }
    return label;
};