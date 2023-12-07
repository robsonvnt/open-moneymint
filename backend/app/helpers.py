import calendar
import datetime
import random
import string


def generate_code(length=10):
    # Definindo os caracteres permitidos: letras maiúsculas, minúsculas e dígitos
    characters = string.ascii_letters + string.digits
    # Gerando o código
    unique_code = ''.join(random.choices(characters, k=length))
    return unique_code


def get_last_day_of_the_month(date_input: datetime.date = None):
    if date_input is None:
        date_input = datetime.date.today()
    year, month = date_input.year, date_input.month
    ultimo_dia = calendar.monthrange(year, month)[1]
    return datetime.date(year, month, ultimo_dia)


def ofx_to_json(ofx_file_path):
    from ofxparse import OfxParser
    import json

    with open(ofx_file_path, 'rb') as file:
        ofx = OfxParser.parse(file)

    transactions_list = []

    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transaction_data = {
                "date": transaction.date.strftime("%Y-%m-%d"),
                "description": transaction.memo,
                "value": float(transaction.amount)
            }
            transactions_list.append(transaction_data)

    return json.dumps(transactions_list, indent=4)
