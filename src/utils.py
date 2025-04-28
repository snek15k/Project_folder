def filter_vacancies(vacancies: list, keyword: str) -> list:
    """Фильтрует вакансии по ключевому слову в описании."""
    return [vac for vac in vacancies if keyword.lower() in vac.description.lower()]


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """Возвращает топ-N вакансий по зарплате."""
    return sorted(vacancies, reverse=True)[:top_n]


def print_vacancies(vacancies: list):
    """Выводит вакансии в удобочитаемом формате."""
    for vac in vacancies:
        print(f"{vac.title} - {vac.salary}\n{vac.url}\n")
