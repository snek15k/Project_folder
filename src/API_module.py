import requests
from abc import ABC, abstractmethod


class JobAPI(ABC):
    """Абстрактный класс для работы с API платформ с вакансиями."""

    @abstractmethod
    def get_vacancies(self, query: str, per_page: int = 20) -> list:
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"  # Приватный атрибут
        self._russia_id = "113"  # ID России в API hh.ru (теперь передается корректно)

    def get_vacancies(self, query: str, per_page: int = 20) -> list:
        """Получение вакансий с hh.ru."""
        params = {"text": query, "per_page": per_page, "area": self._russia_id}
        response = requests.get(self._base_url, params=params)

        if response.status_code != 200:
            raise Exception(f"Ошибка запроса к API hh.ru: {response.status_code}")

        # Получаем данные с API
        data = response.json()

        # Получаем список вакансий
        vacancies_data = data.get("items", [])

        # Обрабатываем зарплату для каждой вакансии
        for vacancy in vacancies_data:
            salary = vacancy.get("salary")
            vacancy["salary"] = self.format_salary(salary) if salary else "Зарплата не указана"

        return vacancies_data

    @staticmethod
    def format_salary(salary: dict) -> str:
        """Форматирование зарплаты в читаемый вид."""
        if salary:
            from_salary = salary.get("from")
            to_salary = salary.get("to")
            currency = salary.get("currency", "не указана")

            if from_salary and to_salary:
                return f"{from_salary} - {to_salary} {currency}"
            if from_salary:
                return f"от {from_salary} {currency}"
            if to_salary:
                return f"до {to_salary} {currency}"
        return "Зарплата не указана"
