from typing import List

from sqlalchemy import Date
from sqlalchemy.exc import NoResultFound

from datetime import date

from finance.domain.category_erros import CategoryUnexpectedError, CategoryNotFound
from finance.domain.models import CategoryModel
from finance.repository.db.db_entities import Category
from investment.helpers import generate_code


class CategoryRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_category_data: CategoryModel) -> Category:
        session = self.session
        try:
            if new_category_data.parent_category_code:
                self.find_by_code(new_category_data.parent_category_code)
            new_category = Category(
                code=generate_code(),
                created_at=date.today(),
                **new_category_data.model_dump(
                    exclude={'code', 'created_at'}
                )
            )
            session.add(new_category)
            session.commit()
            session.refresh(new_category)
            return new_category
        except CategoryNotFound:
            raise CategoryNotFound("Parent Category Not Found")
        except Exception:
            raise CategoryUnexpectedError()

    def find_by_code(self, category_code: str) -> CategoryModel:
        session = self.session
        try:
            category = session.query(Category).filter(
                Category.code == category_code
            ).one()
            return category
        except NoResultFound:
            raise CategoryNotFound()
        except Exception:
            raise CategoryUnexpectedError()

    def update(self, category_code: str, updated_category_data: CategoryModel) -> Category:
        session = self.session
        try:
            category = session.query(Category).filter(
                Category.code == category_code
            ).one()
            for key, value in updated_category_data.dict().items():
                setattr(category, key, value)
            session.commit()
            session.refresh(category)
            return category
        except NoResultFound:
            raise CategoryNotFound()
        except Exception:
            raise CategoryUnexpectedError()

    def delete(self, category_code: str):
        session = self.session
        try:
            main_category: CategoryModel = session.query(Category).filter(
                Category.code == category_code
            ).one()

            children_categories = self.find_all(
                main_category.user_code, category_code
            )
            # Delete children categories
            for child_category in children_categories:
                self.delete(child_category.code)

            session.delete(main_category)
            session.commit()
        except NoResultFound:
            raise CategoryNotFound()
        except Exception:
            raise CategoryUnexpectedError()

    def find_all(self, user_code: str, parent_category_code: str) -> List[CategoryModel]:
        session = self.session
        try:
            categories = session.query(Category).filter(
                Category.user_code == user_code,
                Category.parent_category_code == parent_category_code
            ).all()
            return categories
        except Exception:
            raise CategoryUnexpectedError()
