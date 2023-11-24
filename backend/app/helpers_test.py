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
