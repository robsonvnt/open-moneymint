import argparse

from finance.repository.db.db_connection import get_db_session
from finance.services.factory import ServiceFactory


def process_csv_transactions(csv_path: str, account_code: str, user_code: str):
    with get_db_session() as session:
        financial_transaction_service = ServiceFactory.create_financial_transaction_service(session)
        financial_transaction_service.create_transactions_from_csv(csv_path, account_code, user_code)

def main():
    parser = argparse.ArgumentParser(description="Processa um arquivo CSV para criar transações financeiras.")
    parser.add_argument('csv_path', type=str, help='O caminho para o arquivo CSV')
    parser.add_argument('account_code', type=str, help='O código da conta')
    parser.add_argument('user_code', type=str, help='O código do usuário')

    args = parser.parse_args()
    process_csv_transactions(args.csv_path, args.account_code, args.user_code)

if __name__ == "__main__":
    main()
