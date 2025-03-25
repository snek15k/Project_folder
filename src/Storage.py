import json
from abc import ABC, abstractmethod
from src.Vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **filters) -> list:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        pass


class JSONStorage(VacancyStorage):
    """Класс для работы с JSON-файлом."""

    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename  # Приватный атрибут

    def _load_data(self) -> list:
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: list):
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        data = self._load_data()
        vacancy_dict = vacancy.to_dict()

        if not any(vac["url"] == vacancy_dict["url"] for vac in data):
            data.append(vacancy_dict)
            self._save_data(data)

    def get_vacancies(self, **filters) -> list:
        data = self._load_data()
        vacancies = [Vacancy(**vac) for vac in data]

        for key, value in filters.items():
            vacancies = [vac for vac in vacancies if value.lower() in getattr(vac, key).lower()]

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy):
        data = self._load_data()
        data = [vac for vac in data if vac["url"] != vacancy.url]
        self._save_data(data)
