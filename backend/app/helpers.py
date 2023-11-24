import string
import random
import calendar
import datetime


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
