import React, {useEffect, useState} from 'react';
import {CategoryService} from "../CategoryService";

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import {TreeView} from '@mui/x-tree-view/TreeView';
import {TreeItem} from '@mui/x-tree-view/TreeItem';
import {CategoryInput, CategoryTreeItem} from "../../models";
import IconButton from "@mui/material/IconButton";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import CategoryDialogForm from "./CategoryDialogForm";

interface CategoryTreeProps {
    selectedCategoryCode: string;
    setSelectedCategoryCode: React.Dispatch<React.SetStateAction<string>>;
}

const CategoryTree: React.FC<CategoryTreeProps> =
    ({
         selectedCategoryCode,
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
            setActionButton(selectedCategoryCode === "" ? "create" : "edit")
        }, [selectedCategoryCode]);

        const [actionButton, setActionButton] = React.useState<"edit" | "create">("create");

        const handlerSetSelectedCategoryCode = (category_code: string) => {
            setSelectedCategoryCode(category_code)
            setActionButton("edit")
        }

        // Form
        const [openCategoryForm, setOpenCategoryForm] = useState<boolean>(false);
        const [onCloseAccount, setOnCloseAccount] = useState<boolean>(false);
        const [onSaveAccount, setOnSaveAccount] = useState<boolean>(false);
        const [currentCategory, setCurrentCategory] = useState<CategoryInput>({name: '', parent_category_code: ''});


        const handleClickAdd = () => {
            setCurrentCategory({name: '', parent_category_code: ''})
            setOpenCategoryForm(true);
        };

        const handleClickEdit = () => {
            categoryService.get(selectedCategoryCode).then((cat) => {
                let cmi: CategoryInput = {
                    name: cat.name,
                    parent_category_code: cat.parent_category_code
                }
                setCurrentCategory(cmi);
                setOpenCategoryForm(true);
            });
        };

        const handleOnDelete = () => {
            categoryService.delete(selectedCategoryCode).then(() => {
                loadCategories();
                setSelectedCategoryCode("");
            })
        };

        const handleSaveForm = (newCategory: CategoryInput) => {
            if (selectedCategoryCode === "") {
                categoryService.create(newCategory).then((cateory) => {
                    loadCategories()
                    setSelectedCategoryCode(cateory.code);
                })
            } else {
                categoryService.update(selectedCategoryCode, newCategory).then((cateory) => {
                    loadCategories()
                })
            }
        };

        const onCloseForm = () => {
            setCurrentCategory({name: '', parent_category_code: ''})
            setOpenCategoryForm(false);
        };

        // Tree

        const renderNode = (categoryTree: CategoryTreeItem[]): JSX.Element[] => {
            return categoryTree.map((category) => (
                <TreeItem
                    key={category.code}
                    nodeId={category.code}
                    label={category.name}
                    onClick={() => handlerSetSelectedCategoryCode(category.code)}
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
                    <IconButton onClick={actionButton === "edit" ? handleClickEdit : handleClickAdd}>
                        {actionButton === "edit" ? <EditIcon/> : <AddIcon/>}
                    </IconButton>
                </div>

                <TreeView
                    aria-label="file system navigator"
                    defaultCollapseIcon={<ExpandMoreIcon/>}
                    defaultExpandIcon={<ChevronRightIcon/>}
                    selected={selectedCategoryCode}
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
                    onClose={onCloseForm}
                    onSave={handleSaveForm}
                    onDelete={handleOnDelete}
                    currentCategory={currentCategory}
                    setCurrentCategory={setCurrentCategory}
                    selectedCategoryCode={selectedCategoryCode}
                />
            </>
        );
    }

export default CategoryTree;


