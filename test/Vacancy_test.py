from src.Vacancy import Vacancy


def test_vacancy_initialization():
    """Тестируем инициализацию объекта Vacancy"""
    vacancy = Vacancy(title="Тестировщик", url="http://example.com", salary="50000", description="Описание вакансии")

    assert vacancy.title == "Тестировщик"
    assert vacancy.url == "http://example.com"
    assert vacancy.salary == "50000"
    assert vacancy.description == "Описание вакансии"


def test_vacancy_salary_default():
    """Тестируем, что зарплата по умолчанию равна 'Зарплата не указана'"""
    vacancy = Vacancy(title="Тестировщик", url="http://example.com", salary=None, description="Описание вакансии")

    assert vacancy.salary == "Зарплата не указана"


def test_vacancy_to_dict():
    """Тестируем метод to_dict()"""
    vacancy = Vacancy(title="Тестировщик", url="http://example.com", salary="50000", description="Описание вакансии")

    expected_dict = {
        "title": "Тестировщик",
        "url": "http://example.com",
        "salary": "50000",
        "description": "Описание вакансии"
    }

    assert vacancy.to_dict() == expected_dict


def test_vacancy_comparison_lt():
    """Тестируем сравнение вакансий по зарплате (меньше)"""
    vacancy1 = Vacancy(title="Тестировщик", url="http://example.com", salary="50000", description="Описание вакансии")
    vacancy2 = Vacancy(title="Разработчик", url="http://example.com", salary="60000", description="Описание вакансии")

    assert vacancy1 < vacancy2  # Тестируем что зарплата 50000 меньше 60000


def test_vacancy_comparison_gt():
    """Тестируем сравнение вакансий по зарплате (больше)"""
    vacancy1 = Vacancy(title="Тестировщик", url="http://example.com", salary="60000", description="Описание вакансии")
    vacancy2 = Vacancy(title="Разработчик", url="http://example.com", salary="50000", description="Описание вакансии")

    assert vacancy1 > vacancy2  # Тестируем что зарплата 60000 больше 50000


def test_vacancy_comparison_eq():
    """Тестируем сравнение вакансий по зарплате (равно)"""
    vacancy1 = Vacancy(title="Тестировщик", url="http://example.com", salary="50000", description="Описание вакансии")
    vacancy2 = Vacancy(title="Тестировщик", url="http://example.com", salary="50000", description="Описание вакансии")

    assert vacancy1 == vacancy2  # Тестируем что зарплаты равны


def test_get_salary_value_valid():
    """Тестируем метод get_salary_value для валидных зарплат"""
    vacancy = Vacancy(title="Тестировщик", url="http://example.com", salary="50000", description="Описание вакансии")
    assert vacancy.get_salary_value() == 50000  # Получаем числовое значение зарплаты


def test_get_salary_value_invalid():
    """Тестируем метод get_salary_value для невалидных зарплат"""
    vacancy = Vacancy(title="Тестировщик", url="http://example.com", salary="Зарплата не указана",
                      description="Описание вакансии")
    assert vacancy.get_salary_value() == "Зарплата не указана"  # Получаем строку, если зарплата не числовая
