import requests
from abc import ABC, abstractmethod


class JobAPI(ABC):
    """
    Абстрактный класс для работы с API платформ вакансий.
    """

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 20) -> list:
        """Метод для получения вакансий по запросу."""
        pass


def format_salary(salary_data):
    """Форматирование зарплаты."""
    if not salary_data or (salary_data.get('from') is None and salary_data.get('to') is None):
        return "Зарплата не указана"

    salary_from = salary_data.get('from')
    salary_to = salary_data.get('to')
    currency = salary_data.get('currency', 'N/A')

    # Если зарплата указана от и до
    if salary_from and salary_to:
        return f"{salary_from} - {salary_to} {currency}"
    # Если указана только от
    elif salary_from:
        return f"От {salary_from} {currency}"
    # Если указана только до
    elif salary_to:
        return f"До {salary_to} {currency}"
    else:
        return "Зарплата не указана"


class HeadHunterAPI(JobAPI):
    """
    Класс для работы с API hh.ru.
    """
    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.russia_id = 113  # ID России на hh.ru

    def get_vacancies(self, query: str, per_page: int = 20) -> list:
        """Получение вакансий с hh.ru."""
        params = {"text": query, "per_page": per_page}
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception(f"Ошибка запроса к API hh.ru: {response.status_code}")

        # Получаем данные с API
        data = response.json()

        # Получаем список вакансий
        vacancies_data = data.get("items", [])

        # Фильтруем вакансии по стране (ID страны должен быть 113 для России)
        vacancies_data = [
            vacancy for vacancy in vacancies_data
            if vacancy.get("area") and
            vacancy["area"].get("id") == str(self.russia_id)  # Проверяем ID страны
        ]

        # Обрабатываем зарплату для каждой вакансии
        for vacancy in vacancies_data:
            salary = vacancy.get("salary")
            if salary:
                vacancy['salary'] = format_salary(salary)
            else:
                vacancy['salary'] = "Зарплата не указана"

        return vacancies_data
