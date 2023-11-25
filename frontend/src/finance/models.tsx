export interface AccountModel {
    code: string;
    name: string;
    description: string;
    user_code: string;
    balance: number;
    created_at: string;
}

export interface CategoryModel {
    code: string;
    name: string;
    parent_category_code?: string;
    user_code: string;
    created_at: string;
}

export interface CategoryTreeItem {
    code: string;
    name: string;
    children: CategoryTreeItem[];

}

export interface AccountTransaction {
    code: string;
    account_code: string;
    description: string;
    category_code: string;
    type: string;
    date: string;
    value: number;
}