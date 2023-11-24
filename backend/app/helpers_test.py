import string
import random
from calendar import calendar
import datetime
from unittest.mock import patch, Mock

from helpers import generate_code, get_last_day_of_the_month


def test_generate_code():
    result = generate_code()
    assert len(result) == 10

    result = generate_code(length=20)
    assert len(result) == 20


def test_get_last_day_of_the_month_today():

    date_mock = Mock(wraps=datetime.date)
    date_mock.today.return_value = datetime.date(2023, 2, 15)


    with patch('datetime.datetime.date') as date_mock:
        result = get_last_day_of_the_month()
        assert date_mock.today.calle_count == 10
        assert result == datetime.date(2023, 2, 28)


def test_get_last_day_of_the_month_specifying_the_date():
    specified_date = datetime.date(2023, 1, 15)
    result = get_last_day_of_the_month(specified_date)
    assert result == datetime.date(2023, 1, 31)


