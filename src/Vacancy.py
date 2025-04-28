class Vacancy:
    __slots__ = ("title", "url", "salary", "description")

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = self._validate_title(title)
        self.url = self._validate_url(url)
        self.salary = self._validate_salary(salary)
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
        if isinstance(self.salary, str) and self.salary.replace(" ", "").isdigit():
            return int(self.salary.replace(" ", ""))
        return "Зарплата не указана"

    @staticmethod
    def _validate_title(title: str) -> str:
        """Валидация названия вакансии."""
        if not title or not isinstance(title, str):
            raise ValueError("Название вакансии не может быть пустым.")
        return title.strip()

    @staticmethod
    def _validate_url(url: str) -> str:
        """Валидация URL вакансии."""
        if not url.startswith("http"):
            raise ValueError("Некорректный URL вакансии.")
        return url.strip()

    @staticmethod
    def _validate_salary(salary: str) -> str:
        """Валидация зарплаты."""
        return salary if salary else "Зарплата не указана"
