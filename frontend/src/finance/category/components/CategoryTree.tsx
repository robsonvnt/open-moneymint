import React, {useEffect, useState} from 'react';
import {CategoryService} from "../CategoryService";

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import {TreeView} from '@mui/x-tree-view/TreeView';
import {TreeItem} from '@mui/x-tree-view/TreeItem';
import {CategoryTreeItem} from "../../models";
import IconButton from "@mui/material/IconButton";
import AddIcon from "@mui/icons-material/Add";
import CategoryDialogForm, {NewCategoryModel} from "./CategoryDialogForm";

interface CategoryTreeProps {
    setSelectedCategoryCode: React.Dispatch<React.SetStateAction<string>>;
}

const CategoryTree: React.FC<CategoryTreeProps> =
    ({
         setSelectedCategoryCode
     }) => {
        const categoryService = CategoryService;
        const [categoryTree, setCategoryTree] = React.useState<CategoryTreeItem[]>([]);


        const loadCategories = () => {
            categoryService.getAllCategories().then(categoryTree => {
                setCategoryTree(categoryTree);
            })
        }

        useEffect(() => {
            loadCategories();
        }, []);


        // Form
        const [openCategoryForm, setOpenCategoryForm] = useState<boolean>(false);
        const [onCloseAccount, setOnCloseAccount] = useState<boolean>(false);
        const [onSaveAccount, setOnSaveAccount] = useState<boolean>(false);


        const handleIconClick = () => {
            setOpenCategoryForm(true);
        };

        const onCloseCategoryForm = () => {
            setOpenCategoryForm(false);
        };
        const onSaveCategoryForm = (newCategory: NewCategoryModel) => {
            categoryService.create(newCategory).then((cateory) => {
                loadCategories()
            })
        };

        // Tree

        const renderNode = (categoryTree: CategoryTreeItem[]): JSX.Element[] => {
            return categoryTree.map((category) => (
                <TreeItem
                    key={category.code}
                    nodeId={category.code}
                    label={category.name}
                    onClick={() => setSelectedCategoryCode(category.code)}
                >
                    {category.children && renderNode(category.children)}
                </TreeItem>
            ));
        };

        return (
            <>
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    margin: 0,
                    marginTop: 5
                }}>
                    <div style={{width: 48}}> {/* Ajuste a largura para corresponder à do IconButton */}
                    </div>
                    <h4 style={{
                        margin: 0,
                        flexGrow: 1,
                        textAlign: 'center'
                    }}>
                        Categorias
                    </h4>
                    <IconButton onClick={handleIconClick}>
                        <AddIcon/> {/* Substitua por seu ícone preferido */}
                    </IconButton>
                </div>

                <TreeView
                    aria-label="file system navigator"
                    defaultCollapseIcon={<ExpandMoreIcon/>}
                    defaultExpandIcon={<ChevronRightIcon/>}
                >
                    <TreeItem
                        key="-"
                        nodeId="0"
                        label="Todos"
                        onClick={() => setSelectedCategoryCode("")}
                    >

                    </TreeItem>
                    {renderNode(categoryTree)}
                </TreeView>
                <CategoryDialogForm
                    open={openCategoryForm}
                    onClose={onCloseCategoryForm}
                    onSave={onSaveCategoryForm}
                />
            </>
        );
    }

export default CategoryTree;


