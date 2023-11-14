from sqlalchemy import text

from src.investment.domain.investment_errors import InvestmentNotFound, UnexpectedError, DatabaseError, \
    ColumnDoesNotExistError, NoAssetsFound
from src.investment.domain.models import InvestmentModel
from src.investment.helpers import generate_code
from src.investment.repository.db.db_entities import Investment
from sqlalchemy.exc import NoResultFound


def to_database(investment_model: InvestmentModel) -> Investment:
    return Investment(**investment_model.model_dump())


def to_model(investment: Investment) -> InvestmentModel:
    return InvestmentModel(**investment.to_dict())


# Repositório de Investment
class InvestmentRepo:
    def __init__(self, session):
        self.session = session

    def create(self, new_investment_data):
        session = self.session
        try:
            code = generate_code()
            new_investment = Investment(id=None, **new_investment_data.dict())
            new_investment.code = code
            session.add(new_investment)
            session.commit()
            session.refresh(new_investment)
            return to_model(new_investment)
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                raise InvestmentNotFound()
            else:
                raise DatabaseError()

    def find_by_code(self, investment_code):
        session = self.session
        try:
            investment = session.query(Investment).filter(
                Investment.code == investment_code,
            ).one()
            return to_model(investment)
        except NoResultFound:
            raise InvestmentNotFound()
        except Exception as e:
            raise UnexpectedError()

    def find_by_portf_investment_code(self, portfolio_code: str, investment_code):
        investment = self.find_by_code(investment_code)
        if investment.portfolio_code == portfolio_code:
            return investment
        else:
            raise InvestmentNotFound()

    def find_all_by_portfolio_code(self, portfolio_code: str, order_by: str = None):
        session = self.session
        try:
            query = session.query(Investment).filter(
                Investment.portfolio_code == portfolio_code,
            )
            if order_by:
                order_by_parts = order_by.strip().split('.')
                column_name = order_by_parts[0]
                column = getattr(Investment, column_name)
                if len(order_by_parts) > 1 and order_by_parts[1].lower() == 'desc':
                    column = column.desc()
                query = query.order_by(column)
            return [to_model(inv) for inv in query.all()]
        except AttributeError:
            raise ColumnDoesNotExistError()
        except Exception:
            raise DatabaseError()
        finally:
            session.close()

    def delete(self, portfolio_code: str, investment_code: str):
        session = self.session
        try:
            investment = session.query(Investment).filter(
                Investment.portfolio_code == portfolio_code,
                Investment.code == investment_code
            ).first()
            if investment is None:
                raise InvestmentNotFound()
            session.delete(investment)
            session.commit()
            return True
        except Exception as e:
            raise DatabaseError()
        finally:
            session.close()

    def update(
            self,
            portfolio_code: str,
            investment_code,
            updated_investment_data: InvestmentModel
    ):
        session = self.session
        try:
            investment = session.query(Investment).filter(
                Investment.portfolio_code == portfolio_code,
                Investment.code == investment_code
            ).one()
            for key, value in updated_investment_data.model_dump().items():
                setattr(investment, key, value)
            session.commit()
            session.refresh(investment)
            return to_model(investment)
        except NoResultFound as e:
            raise InvestmentNotFound()
        except Exception as e:
            raise UnexpectedError()
        finally:
            session.close()

    def get_diversification_portfolio(self, portfolio_code):
        session = self.session
        try:
            query = text(
                "SELECT asset_type, SUM(quantity * current_average_price) AS total_weight "
                "FROM investments WHERE portfolio_code = :portfolio_code GROUP BY asset_type"
            )
            result = session.execute(query, {"portfolio_code": portfolio_code}).fetchall()
            if not result:
                raise NoAssetsFound()
            diversification_portfolio = {row[0]: row[1] for row in result}
            return diversification_portfolio
        except Exception as e:
            raise DatabaseError()
        finally:
            session.close()
