from datetime import date

import pytest
from unittest.mock import create_autospec

from finance.domain.category_erros import CategoryNotFound, CategoryUnexpectedError, CategoryOperationNotPermittedError
from finance.domain.models import CategoryModel
from finance.repository.category_repository import CategoryRepo
from finance.services.category_service import CategoryService


@pytest.fixture
def mock_category_repo():
    return create_autospec(CategoryRepo)


@pytest.fixture
def account_service(mock_category_repo):
    return CategoryService(mock_category_repo)


def test_create_category_success(account_service, mock_category_repo):
    category_model = CategoryModel(
        name="Test Category",
        parent_category_code=None,
        user_code="USER123"
    )
    mock_category_repo.create.return_value = category_model

    result = account_service.create(category_model)

    mock_category_repo.create.assert_called_once_with(category_model)
    assert result.name == category_model.name


def test_create_category_not_found_error(account_service, mock_category_repo):
    category_model = CategoryModel(
        name="Test Category",
        parent_category_code="Fake Parent",
        user_code="USER123"
    )
    mock_category_repo.create.side_effect = CategoryNotFound("Category not found")

    with pytest.raises(CategoryNotFound):
        account_service.create(category_model)


def test_update(account_service, mock_category_repo):
    category_model = CategoryModel(
        code="CAT001",
        name="Test Category",
        parent_category_code=None,
        user_code="USER123",
        created_at=date.today()
    )
    mock_category_repo.update.return_value = category_model
    result = account_service.update("CAT001", category_model)

    mock_category_repo.update.assert_called_once_with("CAT001", category_model)
    assert result.name == category_model.name


def test_update_invalid_operation(account_service, mock_category_repo):
    category_model = CategoryModel(
        code="CAT001",
        name="Test Category",
        parent_category_code=None,
        user_code="USER123",
        created_at=date.today()
    )
    mock_category_repo.update.return_value = category_model

    with pytest.raises(CategoryOperationNotPermittedError) as error:
        account_service.update("CAT002", category_model)

    assert "Code cannot be changed" in str(error)
    assert mock_category_repo.update.call_count == 0


def test_delete_category(account_service, mock_category_repo):
    category_code = "CAT123"
    account_service.delete(category_code)

    mock_category_repo.delete.assert_called_once_with("CAT123")


def test_delete_category_failure(account_service, mock_category_repo):
    category_code = "CAT123"
    mock_category_repo.delete.side_effect = CategoryNotFound

    with pytest.raises(CategoryNotFound):
        account_service.delete(category_code)
    mock_category_repo.delete.assert_called_once_with(category_code)


def test_find_all_categories(account_service, mock_category_repo):
    user_code = "UC"
    parent_category_code = "P"
    mock_categories = [
        CategoryModel(name="N1", parent_category_code="P", user_code="UC"),
        CategoryModel(name="N2", parent_category_code="P", user_code="UC"),
    ]
    mock_category_repo.find_all.return_value = mock_categories

    results = account_service.find_all(user_code, parent_category_code)

    mock_category_repo.find_all.assert_called_once_with(user_code, parent_category_code)
    assert len(results) == len(mock_categories)
    assert all(isinstance(category, CategoryModel) for category in results)
