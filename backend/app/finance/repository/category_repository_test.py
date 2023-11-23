from sqlalchemy.exc import NoResultFound

from finance.domain.category_erros import CategoryNotFound
from finance.domain.models import CategoryModel
from finance.repository.category_repository import CategoryRepo
from finance.repository.db.prepare_to_db_test import *


def test_create_category(memory_db_session):
    new_category_data = CategoryModel(
        name="Test Category",
        user_code="USER001",
        parent_category_code=None
    )

    category_repo = CategoryRepo(memory_db_session)
    result = category_repo.create(new_category_data)

    assert result.name == "Test Category"
    assert len(result.code) == 10

    # Test with parent
    another_new_category_data = CategoryModel(
        name="Another Test Category",
        user_code="USER001",
        parent_category_code=result.code
    )
    result = category_repo.create(new_category_data)
    assert result.name == "Test Category"
    assert len(result.code) == 10


def test_create_category_non_existent_parent(memory_db_session):
    category_data = CategoryModel(
        name="Test Category",
        user_code="USER001",
        parent_category_code="non_existent"
    )
    category_repo = CategoryRepo(memory_db_session)

    with pytest.raises(CategoryNotFound) as error:
        category_repo.create(category_data)

    assert "Parent Category Not Found" in str(error)


def test_find_by_code(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)
    result = category_repo.find_by_code("CAT001")

    assert result.code == "CAT001"
    assert result.name == "Main Category"


def test_find_by_non_existent_code(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)

    with pytest.raises(CategoryNotFound):
        category_repo.find_by_code("non_existent_code")


def test_update_category(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)
    updated_category = CategoryModel(
        code="CAT001",
        name="Updated Category",
        user_code="USER001",
        parent_category_code=None
    )

    result = category_repo.update("CAT001", updated_category)
    assert result.name == "Updated Category"


def test_update_non_existent_category(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)
    updated_category = CategoryModel(
        code="CAT001",
        name="Updated Category",
        user_code="USER001",
        parent_category_code=None
    )

    with pytest.raises(CategoryNotFound):
        category_repo.update("non_existent", updated_category)


def test_delete_category(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)

    category_repo.delete("CAT002")

    # Here it tests whether the item was deleted
    with pytest.raises(NoResultFound):
        memory_db_session.query(Category).filter(
            Category.code == "CAT002"
        ).one()

    category_repo.delete("CAT001")

    # here tests whether the deletion is occurring at all CAT001 children
    for i in range(3, 5):
        with pytest.raises(NoResultFound):
            memory_db_session.query(Category).filter(
                Category.code == f"CAT00{i}"
            ).one()

    # CAT009 is a son of category 3 which is a daughter of category 001
    # here tests whether the deletion is occurring at all levels of children
    with pytest.raises(NoResultFound):
        memory_db_session.query(Category).filter(
            Category.code == f"CAT009"
        ).one()


def test_find_all_categories(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)

    results = category_repo.find_all(
        "USER001",
        "CAT001"
    )

    assert len(results) == 3
    assert results[0].code == "CAT002"
    assert results[1].code == "CAT003"
    assert results[2].code == "CAT004"


def test_find_all_categories_with_none_parent(memory_db_session):
    add_categories(memory_db_session)
    category_repo = CategoryRepo(memory_db_session)

    results = category_repo.find_all(
        "USER001",None
    )

    assert len(results) == 4
    assert results[0].code == "CAT001"
    assert results[1].code == "CAT005"
    assert results[2].code == "CAT006"
    assert results[3].code == "CAT007"
