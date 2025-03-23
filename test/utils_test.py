import pytest
from src.Vacancy import Vacancy
from src.utils import filter_vacancies, get_top_vacancies, print_vacancies


@pytest.fixture
def vacancies():
    return [
        Vacancy(title="Вакансия 1", url="https://example.com/vacancy1", salary="50000",
                description="Описание вакансии для программиста"),
        Vacancy(title="Вакансия 2", url="https://example.com/vacancy2", salary="60000",
                description="Описание вакансии для тестировщика"),
        Vacancy(title="Вакансия 3", url="https://example.com/vacancy3", salary="70000",
                description="Описание вакансии для аналитика"),
        Vacancy(title="Вакансия 4", url="https://example.com/vacancy4", salary="55000",
                description="Программист на Python"),
    ]


def test_filter_vacancies(vacancies):
    # Фильтруем вакансии по ключевому слову "программист"
    filtered_vacancies = filter_vacancies(vacancies, "программист")
    assert len(filtered_vacancies) == 2  # Должно быть две вакансии, связанные с программированием
    assert all("программист" in vac.description.lower() for vac in
               filtered_vacancies)  # Все вакансии должны содержать слово "программист"


def test_filter_vacancies_no_match(vacancies):
    # Фильтруем вакансии по ключевому слову, которого нет в описаниях
    filtered_vacancies = filter_vacancies(vacancies, "дизайнер")
    assert len(filtered_vacancies) == 0  # Должно быть 0 вакансий, так как слово "дизайнер" не встречается


def test_get_top_vacancies(vacancies):
    # Получаем топ-3 вакансии по зарплате
    top_vacancies = get_top_vacancies(vacancies, 3)
    assert len(top_vacancies) == 3  # Должны быть 3 вакансии
    assert top_vacancies[0].salary == "70000"  # Первая вакансия должна быть с самой высокой зарплатой
    assert top_vacancies[1].salary == "60000"  # Вторая вакансия с меньшей зарплатой
    assert top_vacancies[2].salary == "55000"  # Третья вакансия с самой низкой зарплатой


def test_get_top_vacancies_less_than_n(vacancies):
    # Получаем топ-10 вакансий (больше, чем в списке вакансий)
    top_vacancies = get_top_vacancies(vacancies, 10)
    assert len(top_vacancies) == len(vacancies)  # Должно быть столько вакансий, сколько есть в списке
    assert top_vacancies[0].salary == "70000"  # Первая вакансия с самой высокой зарплатой


def test_print_vacancies(capsys, vacancies):
    # Проверяем вывод вакансий с использованием фикстуры capsys
    print_vacancies(vacancies)

    captured = capsys.readouterr()
    # Проверяем, что в выводе содержатся все названия вакансий
    for vac in vacancies:
        assert vac.title in captured.out
        assert vac.salary in captured.out
        assert vac.url in captured.out
