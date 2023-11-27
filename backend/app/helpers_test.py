import json
import random
from calendar import calendar
import datetime
from unittest.mock import patch, Mock

from helpers import generate_code, get_last_day_of_the_month, ofx_to_json


def test_generate_code():
    result = generate_code()
    assert len(result) == 10

    result = generate_code(length=20)
    assert len(result) == 20


def test_get_last_day_of_the_month_today():
    fixed_date = datetime.date(2023, 2, 15)

    with patch('datetime.date') as mock_date:
        mock_date.today.return_value = fixed_date
        result = get_last_day_of_the_month()

        assert mock_date.today.call_count == 1
        assert result == datetime.date(2023, 2, 28)


def test_get_last_day_of_the_month_specifying_the_date():
    specified_date = datetime.date(2023, 1, 15)
    result = get_last_day_of_the_month(specified_date)
    assert result == datetime.date(2023, 1, 31)


def test_ofx_to_json():
    import os

    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    ofx_file_path = f'{current_directory}/../tests/data/exemple_file.ofx'

    # Chama a função
    result = ofx_to_json(ofx_file_path)

    # Carrega o resultado como JSON para verificar
    data = json.loads(result)

    # Aqui você pode adicionar asserções específicas baseadas no conteúdo esperado
    # do seu arquivo OFX de exemplo
    assert isinstance(data, list)
    assert len(data) > 0  # Verifica se há pelo menos uma transação

    # Verificações específicas (ajuste conforme necessário)
    # Exemplo: verificar se a primeira transação tem os campos esperados
    assert 'date' in data[0]
    assert 'description' in data[0]
    assert 'value' in data[0]

    # Verificações de valor específico (ajuste com base no seu arquivo OFX de exemplo)
    assert data[0]['date'] == '2023-09-01'
    assert data[0]['description'] == 'Pagamento de conta - Empresa X'
    assert data[0]['value'] == -500.0

