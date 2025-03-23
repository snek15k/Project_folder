import pytest
from unittest.mock import patch, MagicMock
from requests.models import Response

from src.API_module import HeadHunterAPI, format_salary


@pytest.fixture
def mock_get_success():
    """Фикстура для успешного ответа от API"""
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "id": "123",
                "name": "Программист Python",
                "area": {"id": "113", "name": "Россия"},
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"}
            },
            {
                "id": "124",
                "name": "Веб-разработчик",
                "area": {"id": "113", "name": "Россия"},
                "salary": None
            }
        ]
    }
    return mock_response


@pytest.fixture
def mock_get_invalid_country():
    """Фикстура для ответа от API с неправильным ID страны"""
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "id": "123",
                "name": "Программист Python",
                "area": {"id": "1", "name": "Москва"},
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"}
            }
        ]
    }
    return mock_response


def test_get_vacancies_success(mock_get_success):
    """Тест успешного получения вакансий"""
    with patch("requests.get", return_value=mock_get_success):
        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("Программист", per_page=2)

    # Проверка, что запрос был успешным и данные правильно обработаны
    assert len(vacancies) == 2
    assert vacancies[0]['salary'] == "100000 - 150000 RUR"
    assert vacancies[1]['salary'] == "Зарплата не указана"


def test_get_vacancies_invalid_country(mock_get_invalid_country):
    """Тест фильтрации вакансий по неправильному ID страны"""
    with patch("requests.get", return_value=mock_get_invalid_country):
        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies("Программист", per_page=2)

    # Проверка, что вакансии не отфильтровались по ID России
    assert len(vacancies) == 0


@pytest.mark.parametrize(
    "salary_data, expected_output",
    [
        ({"from": 50000, "to": 100000, "currency": "RUR"}, "50000 - 100000 RUR"),
        ({"from": 50000, "currency": "RUR"}, "От 50000 RUR"),
        ({"to": 100000, "currency": "RUR"}, "До 100000 RUR"),
        ({}, "Зарплата не указана"),
        (None, "Зарплата не указана")
    ]
)
def test_format_salary(salary_data, expected_output):
    """Тестирование функции форматирования зарплаты"""
    formatted_salary = format_salary(salary_data)
    assert formatted_salary == expected_output
