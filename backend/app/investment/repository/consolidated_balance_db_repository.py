from datetime import date
from typing import List, Optional
from sqlalchemy import Date
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from investment.domain.consolidated_balance_errors import ConsolidatedPortfolioDatabaseError, \
    ConsolidatedPortfolioUnexpectedError, ConsolidatedPortfolioNotFound
from investment.domain.models import ConsolidatedPortfolioModel
from investment.repository.db.db_entities import ConsolidatedPortfolio


# Function to convert domain model to database model
def to_database(cbp_model: ConsolidatedPortfolioModel) -> ConsolidatedPortfolio:
    return ConsolidatedPortfolio(id=None, **cbp_model.dict())


# Function to convert database model to domain model
def to_model(cbp: ConsolidatedPortfolio) -> ConsolidatedPortfolioModel:
    return ConsolidatedPortfolioModel(**cbp.__dict__)


# Repositório para interagir com a tabela consolidated_balance_portfolios
class ConsolidatedBalanceRepo:
    def __init__(self, session):
        self.session = session

    def filter_by_date_range(
            self,
            portfolio_code: str,
            start_date: Optional[Date] = None,
            end_date: Optional[Date] = None
    ) -> List[ConsolidatedPortfolioModel]:
        """
        Filters the ConsolidatedBalancePortfolio by date range.
        """
        session = self.session
        try:
            query = session.query(ConsolidatedPortfolio).filter(
                ConsolidatedPortfolio.portfolio_code == portfolio_code
            )

            if start_date is not None:
                query = query.filter(ConsolidatedPortfolio.date >= start_date)

            if end_date is not None:
                query = query.filter(ConsolidatedPortfolio.date <= end_date)

            query = query.order_by(ConsolidatedPortfolio.date.asc())
            return [to_model(cbp) for cbp in query.all()]
        except SQLAlchemyError:
            raise ConsolidatedPortfolioDatabaseError()
        except Exception:
            raise ConsolidatedPortfolioUnexpectedError()

    def __get_consolidated_portfolio(
            self, session, portfolio_code: str, date: date
    ) -> ConsolidatedPortfolio:
        try:
            consolidated_portfolio = session.query(ConsolidatedPortfolio) \
                .filter(ConsolidatedPortfolio.date == date) \
                .filter(ConsolidatedPortfolio.portfolio_code == portfolio_code) \
                .one()
            return consolidated_portfolio
        except NoResultFound:
            raise ConsolidatedPortfolioNotFound()
        except SQLAlchemyError:
            raise ConsolidatedPortfolioDatabaseError()
        except Exception:
            raise ConsolidatedPortfolioUnexpectedError()

    def create_or_update(
            self,
            cpm: ConsolidatedPortfolioModel
    ) -> ConsolidatedPortfolioModel:
        session = self.session
        try:
            result = self.__get_consolidated_portfolio(session, cpm.portfolio_code, date.today())
            consolidated_portfolio = result
            consolidated_portfolio.balance = cpm.balance
            consolidated_portfolio.amount_invested = cpm.amount_invested
            session.refresh(consolidated_portfolio)
            return to_model(consolidated_portfolio)
        except ConsolidatedPortfolioNotFound:
            consolidated_portfolio = to_database(cpm)
            session.add(consolidated_portfolio)
            to_model(consolidated_portfolio)
            return to_model(consolidated_portfolio)
        except SQLAlchemyError:
            raise ConsolidatedPortfolioDatabaseError()
        except Exception as e:
            raise ConsolidatedPortfolioUnexpectedError
        finally:
            session.commit()
