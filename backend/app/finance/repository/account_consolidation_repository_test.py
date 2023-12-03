from sqlalchemy.exc import NoResultFound

from finance.domain.account_erros import AccountConsolidationAlreadyExists, AccountConsolidationNotFound
from finance.repository.db.prepare_to_db_test import *

from finance.domain.models import AccountConsolidationModel
from finance.repository.account_consolidation_repository import AccountConsolidationRepo
from finance.repository.db.db_entities import AccountConsolidation


def test_create_consolidation(memory_db_session):
    consolidation_repo = AccountConsolidationRepo(memory_db_session)
    new_consolidated_data = AccountConsolidationModel(
        account_code="ACC001",
        month=date(2023, 12, 3),
        balance=150
    )

    consolidation_repo.create(new_consolidated_data)

    memory_db_session.query(AccountConsolidation).filter(
        AccountConsolidation.account_code == "ACC001"
    ).one()


def test_create_exists_consolidation(memory_db_session):
    consolidation_repo = AccountConsolidationRepo(memory_db_session)
    new_consolidated_data = AccountConsolidationModel(
        account_code="ACC001",
        month=date(2023, 12, 3),
        balance=150
    )
    memory_db_session.add = Mock(side_effect=NoResultFound)

    with pytest.raises(AccountConsolidationAlreadyExists):
        consolidation_repo.create(new_consolidated_data)


def test_update(memory_db_session):
    consolidation_repo = AccountConsolidationRepo(memory_db_session)
    new_consolidated_data = AccountConsolidationModel(
        account_code="ACC001",
        month=date(2023, 12, 3),
        balance=150
    )
    consolidation_repo.create(new_consolidated_data)

    new_consolidated_data.balance = 999
    consolidation_repo.update(new_consolidated_data)

    updated = memory_db_session.query(AccountConsolidation).filter(
        AccountConsolidation.account_code == "ACC001"
    ).one()

    assert updated.balance == 999


def test_update_no_results_found(memory_db_session):
    consolidation_repo = AccountConsolidationRepo(memory_db_session)
    new_consolidated_data = AccountConsolidationModel(
        account_code="ACC001",
        month=date(2023, 12, 3),
        balance=150
    )

    with pytest.raises(AccountConsolidationNotFound):
        consolidation_repo.update(new_consolidated_data)


def test_find_by_account_date(memory_db_session):
    add_account_consolidations(memory_db_session)
    consolidation_repo = AccountConsolidationRepo(memory_db_session)

    consolidation = consolidation_repo.find_by_account_month("ACC001", date(2023, 8, 1))

    assert consolidation.balance == 100


def test_find_by_account_date_not_found(memory_db_session):
    consolidation_repo = AccountConsolidationRepo(memory_db_session)

    with pytest.raises(AccountConsolidationNotFound):
        consolidation_repo.find_by_account_month("ACC001", date(2023, 5, 1))


def test_find_all_by_account(memory_db_session):
    add_account_consolidations(memory_db_session)
    consolidation_repo = AccountConsolidationRepo(memory_db_session)

    consolidations = consolidation_repo.find_all_by_account("ACC001")

    assert len(consolidations) == 3