from src.API_module import HeadHunterAPI
from src.Vacancy import Vacancy
from src.Storage import JSONStorage
from src.utils import filter_vacancies, get_top_vacancies, print_vacancies


def main():
    # Инициализация API и хранилища
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    # Ввод данных от пользователя
    query = input("Введите поисковый запрос: ")
    per_page = int(input("Введите количество вакансий для вывода: "))
    keyword = input("Введите ключевое слово для фильтрации вакансий: ")
    top_n = int(input("Введите количество вакансий для вывода в топ: "))

    # Получаем вакансии с hh.ru
    vacancies_data = hh_api.get_vacancies(query, per_page)

    # Преобразуем вакансии в объекты Vacancy и добавляем в хранилище
    for vac_data in vacancies_data:
        salary = vac_data.get("salary", "Зарплата не указана")
        vacancy = Vacancy(
            title=vac_data["name"],
            url=vac_data["alternate_url"],
            salary=salary,
            description=vac_data["snippet"].get("responsibility", "Описание не указано")
        )
        storage.add_vacancy(vacancy)

    # Получаем все вакансии из хранилища
    stored_vacancies = storage.get_vacancies()

    # Фильтруем вакансии по ключевому слову
    filtered_vacancies = filter_vacancies(stored_vacancies, keyword)

    # Получаем топ-N вакансий по зарплате
    top_vacancies = get_top_vacancies(filtered_vacancies, top_n)

    # Выводим вакансии в удобном формате
    print("\nТоп вакансий по зарплате:")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    main()
