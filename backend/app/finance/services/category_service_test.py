from datetime import date
from unittest.mock import create_autospec, Mock

import pytest

from finance.domain.category_erros import CategoryNotFound, CategoryOperationNotPermittedError
from finance.domain.models import CategoryModel
from finance.repository.category_repository import CategoryRepo
from finance.repository.financial_transaction_repository import FinancialTransactionRepo
from finance.services.category_service import CategoryService


@pytest.fixture
def mock_category_repo():
    return create_autospec(CategoryRepo)


@pytest.fixture
def mock_transaction_repo():
    return create_autospec(FinancialTransactionRepo)


@pytest.fixture
def category_service(mock_category_repo, mock_transaction_repo):
    return CategoryService(mock_category_repo, mock_transaction_repo)


def test_create_category_success(category_service, mock_category_repo):
    category_model = CategoryModel(
        name="Test Category",
        parent_category_code=None,
        user_code="USER123"
    )
    mock_category_repo.create.return_value = category_model

    result = category_service.create(category_model)

    mock_category_repo.create.assert_called_once_with(category_model)
    assert result.name == category_model.name


def test_create_category_not_found_error(category_service, mock_category_repo):
    category_model = CategoryModel(
        name="Test Category",
        parent_category_code="Fake Parent",
        user_code="USER123"
    )
    mock_category_repo.create.side_effect = CategoryNotFound("Category not found")

    with pytest.raises(CategoryNotFound):
        category_service.create(category_model)


def test_update(category_service, mock_category_repo):
    category_model = CategoryModel(
        code="CAT001",
        name="Test Category",
        parent_category_code=None,
        user_code="USER123",
        created_at=date.today()
    )
    mock_category_repo.update.return_value = category_model
    result = category_service.update("CAT001", category_model)

    mock_category_repo.update.assert_called_once_with("CAT001", category_model)
    assert result.name == category_model.name


def test_update_invalid_operation(category_service, mock_category_repo):
    category_model = CategoryModel(
        code="CAT001",
        name="Test Category",
        parent_category_code=None,
        user_code="USER123",
        created_at=date.today()
    )
    mock_category_repo.update.return_value = category_model

    with pytest.raises(CategoryOperationNotPermittedError) as error:
        category_service.update("CAT002", category_model)

    assert "Code cannot be changed" in str(error)
    assert mock_category_repo.update.call_count == 0


def test_delete_category(category_service, mock_category_repo, mock_transaction_repo):
    category_code = "CAT123"
    mock_transaction = Mock()
    mock_transaction.code = "TRA001"
    mock_transaction.category_code = category_code
    mock_transaction_repo.filter.return_value = [mock_transaction]

    category_service.delete(category_code)
    mock_transaction_repo.filter.assert_called_once()
    mock_transaction_repo.update.assert_called_once()
    mock_category_repo.delete.assert_called_once_with("CAT123")


def test_delete_category_failure(category_service, mock_category_repo):
    category_code = "CAT123"
    mock_category_repo.delete.side_effect = CategoryNotFound

    with pytest.raises(CategoryNotFound):
        category_service.delete(category_code)
    mock_category_repo.delete.assert_called_once_with(category_code)


def test_find_categories_by_user_and_parent(category_service, mock_category_repo):
    user_code = "UC"
    parent_category_code = "P"
    mock_categories = [
        CategoryModel(name="N1", parent_category_code="P", user_code="UC"),
        CategoryModel(name="N2", parent_category_code="P", user_code="UC"),
    ]
    mock_category_repo.find_categories_by_user_and_parent.return_value = mock_categories

    results = category_service.find_categories_by_user_and_parent(user_code, parent_category_code)

    mock_category_repo.find_categories_by_user_and_parent.assert_called_once_with(user_code, parent_category_code)
    assert len(results) == len(mock_categories)
    assert all(isinstance(category, CategoryModel) for category in results)


def test_find_all_by_user(category_service, mock_category_repo):
    user_code = "UC"
    parent_category_code = "P"
    mock_categories = [
        CategoryModel(name="N1", parent_category_code="P", user_code="UC"),
        CategoryModel(name="N2", parent_category_code="P", user_code="UC"),
    ]
    mock_category_repo.find_all_by_user.return_value = mock_categories

    results = category_service.find_all_by_user(user_code)

    mock_category_repo.find_all_by_user.assert_called_once_with(user_code)
    assert len(results) == len(mock_categories)
    assert all(isinstance(category, CategoryModel) for category in results)


def test_list_all_children(category_service, mock_category_repo):
    mock_categories = [
        CategoryModel(code="CAT-N1", name="N1", parent_category_code=None, user_code="UC"),
        CategoryModel(code="CAT-N2", name="N2", parent_category_code=None, user_code="UC"),
        CategoryModel(code="CAT-N2.1", name="N2.1", parent_category_code="CAT-N2", user_code="UC"),
        CategoryModel(code="CAT-N1.1", name="N1.1", parent_category_code="CAT-N1", user_code="UC"),
        CategoryModel(code="CAT-N1.2", name="N1.2", parent_category_code="CAT-N1", user_code="UC"),
        CategoryModel(code="CAT-N1.2.1", name="N1.2.1", parent_category_code="CAT-N1.2", user_code="UC"),
    ]
    mock_category_repo.find_all_by_user.return_value = mock_categories

    result = category_service.list_all_children("CAT-N1", "UC")
    assert len(result) == 3
    for cat in result:
        assert cat.name in ["N1", "N1.1", "N1.2", "N1.2.1"]
