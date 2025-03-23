import pytest
import os
from src.Vacancy import Vacancy
from src.Storage import JSONStorage


@pytest.fixture
def storage():
    # Создаем временный JSONStorage для каждого теста
    storage = JSONStorage("test_vacancies.json")
    yield storage
    # Удаляем файл после каждого теста
    if os.path.exists("test_vacancies.json"):
        os.remove("test_vacancies.json")


@pytest.fixture
def vacancy():
    return Vacancy(
        title="Тестовая вакансия",
        url="https://example.com/vacancy1",
        salary="50000",
        description="Описание тестовой вакансии"
    )


def test_add_vacancy(storage, vacancy):
    # Проверяем, что вакансия добавляется в хранилище
    storage.add_vacancy(vacancy)

    # Получаем вакансии из хранилища
    vacancies = storage.get_vacancies()

    assert len(vacancies) == 1  # Должна быть только одна вакансия
    assert vacancies[0].title == vacancy.title  # Проверяем совпадение данных
    assert vacancies[0].url == vacancy.url  # Проверяем URL вакансии


def test_add_duplicate_vacancy(storage, vacancy):
    # Добавляем вакансию дважды
    storage.add_vacancy(vacancy)
    storage.add_vacancy(vacancy)

    # Получаем вакансии из хранилища
    vacancies = storage.get_vacancies()

    assert len(vacancies) == 1  # Вакансия должна быть только одна, даже если добавлена дважды


def test_get_vacancies_with_filters(storage, vacancy):
    # Добавляем несколько вакансий
    storage.add_vacancy(vacancy)

    second_vacancy = Vacancy(
        title="Другая вакансия",
        url="https://example.com/vacancy2",
        salary="60000",
        description="Описание другой вакансии"
    )
    storage.add_vacancy(second_vacancy)

    # Получаем вакансии с фильтром по названию
    filtered_vacancies = storage.get_vacancies(title="Тестовая вакансия")

    assert len(filtered_vacancies) == 1  # Должна быть только одна вакансия с таким названием
    assert filtered_vacancies[0].title == "Тестовая вакансия"  # Проверяем правильность


def test_delete_vacancy(storage, vacancy):
    # Добавляем вакансию
    storage.add_vacancy(vacancy)

    # Получаем все вакансии до удаления
    vacancies_before = storage.get_vacancies()

    # Удаляем вакансию
    storage.delete_vacancy(vacancy)

    # Получаем вакансии после удаления
    vacancies_after = storage.get_vacancies()

    assert len(vacancies_after) == len(vacancies_before) - 1  # Количество вакансий должно уменьшиться на 1
    assert all(vac.url != vacancy.url for vac in vacancies_after)  # В вакансии не должно быть удаленной


def test_get_vacancies_empty(storage):
    # Проверяем, что при отсутствии вакансий возвращается пустой список
    vacancies = storage.get_vacancies()
    assert vacancies == []  # Список вакансий должен быть пустым
