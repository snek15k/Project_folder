class Vacancy:
    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = salary if salary else "Зарплата не указана"  # Убедимся, что тут всегда строка
        self.description = description

    def to_dict(self) -> dict:
        """Преобразует объект вакансии в словарь."""
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description
        }

    def __lt__(self, other):
        return self.get_salary_value() < other.get_salary_value()

    def __gt__(self, other):
        return self.get_salary_value() > other.get_salary_value()

    def __eq__(self, other):
        return self.get_salary_value() == other.get_salary_value()

    def get_salary_value(self) -> int | str:
        """Возвращает числовое значение зарплаты (если указано), иначе сообщение 'Зарплата не указана'."""
        if isinstance(self.salary, str) and self.salary.isdigit():
            return int(self.salary)
        return "Зарплата не указана"  # Если зарплата не указана или не числовая
