import React, {useEffect, useState} from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Grid,
    InputAdornment
} from '@mui/material';
import MenuItem from "@mui/material/MenuItem";
import {CategoryTreeItem} from "../../models";
import {CategoryService} from "../CategoryService";

export interface NewCategoryModel {
    name: string;
    parent_category_code?: string;
}

interface FormErrors {
    name?: string;
    parent_category_code?: string;
}

interface AccountDialogFormProps {
    open: boolean;
    onClose: () => void;
    onSave: (account: NewCategoryModel) => void;
}

const CategoryDialogForm: React.FC<AccountDialogFormProps> = ({open, onClose, onSave}) => {
    const [newCategory, setNewCategory] = useState<NewCategoryModel>({name: '', parent_category_code: ''});
    const [errors, setErrors] = useState<FormErrors>({});
    const [categoryList, setCategoryList] = React.useState<CategoryTreeItem[]>([]);
    const categoryService = CategoryService;

    const prepareCategoryList = (parentName: string, categoryList: CategoryTreeItem[]): CategoryTreeItem[] => {
        let newCategoryList: CategoryTreeItem[] = [];
        categoryList.map(category => {
            let newCategory: CategoryTreeItem = {
                code: category.code,
                name: parentName != "" ? `${parentName} > ${category.name}` : category.name,
                children: []
            }
            newCategoryList.push(newCategory)
            if (category.children.length > 0) {
                let childrenItems = prepareCategoryList(newCategory.name, category.children);
                childrenItems.map(cat => {
                    newCategoryList.push(cat)
                })
            }
        })
        return newCategoryList;
    };

    useEffect(() => {
        categoryService.getAllCategories()
            .then(categoryList => {
                let newCategoryList = prepareCategoryList("", categoryList);
                setCategoryList(newCategoryList);
            });
    }, []);

    const clearForm = () => {
        setNewCategory({name: ""});
        setErrors({});
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNewCategory({...newCategory, [e.target.name]: e.target.value});
    };

    const handleClose = () => {
        onClose();
        clearForm()
    };

    const handleSave = () => {
        if (validate()) {
            onSave(newCategory);
            onClose();
            clearForm()
        }
    };

    const validate = (): boolean => {
        let tempErrors: FormErrors = {};
        tempErrors.name = newCategory.name ? "" : "Campo é obrigatório";

        setErrors(tempErrors);
        return Object.keys(tempErrors).every(key => tempErrors[key as keyof FormErrors] === "");
    }

    return (
        <Dialog open={open} onClose={handleClose}>
            <DialogTitle>Adicionar Nova Categoria</DialogTitle>
            <DialogContent>

                <Grid container
                      spacing={2}
                      alignItems="center"
                >
                    <Grid item xs={12} sm={12}>
                        <TextField
                            autoFocus
                            margin="dense"
                            name="name"
                            label="Nome"
                            type="text"
                            fullWidth
                            value={newCategory.name}
                            onChange={handleChange}
                            error={Boolean(errors.name)}
                            helperText={errors.name || ""}
                        />
                    </Grid>
                    <Grid item xs={12} sm={12}>
                        <TextField
                            select
                            margin="dense"
                            name="category_code"
                            label="Categoria Mãe"
                            value={newCategory.parent_category_code}
                            error={Boolean(errors.parent_category_code)}
                            helperText={errors.parent_category_code || ""}
                            onChange={(e) =>
                                setNewCategory({
                                    ...newCategory,
                                    parent_category_code: e.target.value,
                                })}
                            fullWidth
                        >
                            {categoryList.map((option) => (
                                <MenuItem key={option.code} value={option.code}>
                                    {option.name}
                                </MenuItem>
                            ))}

                        </TextField>
                    </Grid>
                </Grid>


            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Cancelar</Button>
                <Button onClick={handleSave}>Salvar</Button>
            </DialogActions>
        </Dialog>
    );
};

export default CategoryDialogForm;
