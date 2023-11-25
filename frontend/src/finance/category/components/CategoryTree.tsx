import React, {useEffect} from 'react';
import {CategoryService} from "../CategoryService";

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import {TreeView} from '@mui/x-tree-view/TreeView';
import {TreeItem} from '@mui/x-tree-view/TreeItem';
import {CategoryTreeItem} from "../../models";

interface CategoryTreeProps {
    selectedCategoryCode: string;
}

const CategoryTree: React.FC<CategoryTreeProps> = ({selectedCategoryCode}) => {
    const categoryService = CategoryService;
    const [categoryTree, setCategoryTree] = React.useState<CategoryTreeItem[]>([]);


    useEffect(() => {
        categoryService.getAllCategories().then(categoryTree => {
            setCategoryTree(categoryTree);
        })
    }, []);


    const renderNode = (categoryTree: CategoryTreeItem[]): JSX.Element[] => {
        return categoryTree.map((category) => (
            <TreeItem key={category.code} nodeId={category.code} label={category.name}>
                {category.children && renderNode(category.children)}
            </TreeItem>
        ));
    };

    return (
        <>
            <center>
                <h4
                style={{marginBottom: 8}}
                >
                    Categorias
                </h4>
            </center>
            <TreeView
                aria-label="file system navigator"
                defaultCollapseIcon={<ExpandMoreIcon/>}
                defaultExpandIcon={<ChevronRightIcon/>}
            >
                {renderNode(categoryTree)}
            </TreeView>
        </>
    );
}

export default CategoryTree;


