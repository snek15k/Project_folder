import pytest
from unittest.mock import Mock
from src.API_module import HeadHunterAPI


@pytest.fixture
def api():
    """Создаем и возвращаем экземпляр HeadHunterAPI для использования в тестах."""
    return HeadHunterAPI()


def test_get_vacancies_success(api, mocker):
    """Тест на успешное получение вакансий."""
    # Мокируем успешный ответ от API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123456",
                "salary": {"from": 100000, "to": 150000, "currency": "RUB"},
                "snippet": {"responsibility": "Разработка на Python"}
            }
        ]
    }

    mocker.patch("requests.get", return_value=mock_response)

    # Выполним запрос вакансий
    vacancies = api.get_vacancies("Python Developer", 1)

    # Проверим, что вакансии получены правильно
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[0]["salary"] == "100000 - 150000 RUB"


def test_get_vacancies_error(api, mocker):
    """Тест на ошибку при запросе к API."""
    # Мокируем ответ с ошибкой (не 200 статус)
    mock_response = Mock()
    mock_response.status_code = 500
    mocker.patch("requests.get", return_value=mock_response)

    # Проверим, что при ошибке выбрасывается исключение
    with pytest.raises(Exception) as excinfo:
        api.get_vacancies("Python Developer", 1)
    assert str(excinfo.value) == "Ошибка запроса к API hh.ru: 500"


def test_format_salary(api):
    """Тест на форматирование зарплаты."""
    salary = {"from": 100000, "to": 150000, "currency": "RUB"}
    formatted_salary = api.format_salary(salary)
    assert formatted_salary == "100000 - 150000 RUB"

    salary = {"from": 100000, "currency": "RUB"}
    formatted_salary = api.format_salary(salary)
    assert formatted_salary == "от 100000 RUB"

    salary = {"to": 150000, "currency": "RUB"}
    formatted_salary = api.format_salary(salary)
    assert formatted_salary == "до 150000 RUB"

    salary = None
    formatted_salary = api.format_salary(salary)
    assert formatted_salary == "Зарплата не указана"
