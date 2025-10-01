from bd import creating_bd, create_table
from vacancy_processor import connect_api
from manager import DBManager


def user_managment():
    """ Функция взаимодействует с пользователем"""
    db_manager = DBManager()
    try:
        while True:
            print("\nВыберите действие:")
            print('Нажмите: 1 - если хотите Получить список всех компаний и количество Вакансий')
            print('Нажмите: 2 - если хотите Получить всю информацию о Вакансиях')
            print('Нажмите: 3 - если хотите Получить среднюю зарплату по Вакансиям')
            print('Нажмите: 4 - если хотите получить вакансии с зарплатой выше средней')
            print('Нажмите: 5 - если хотите Получить Вакансию по ключевому слову')
            print('Нажмите: 6 - если хотите Выйти')

            choice = input("Введите номер действия: ")
            if choice == '1':
                companies_count = db_manager.get_companies_and_vacancies_count()
                print('Количество вакансий у компаний: ')
                for company, count in companies_count:
                    print(f'Компания {company}:{count} вакансий')
            elif choice == '2':
                company_info = db_manager.get_all_vacancies()
                print('Информация о Вакансиях: ')
                for company, vacancy, link, salary in company_info:
                    print(f'Компания - {company}:Вакансия - {vacancy} Ссылка: {link}, Зарплата: {salary if salary is not None else "Не указана"}\n')
            elif choice == '3':
                avg = db_manager.get_avg_salary()
                print(f'Средняя заработная плата по всем вакансиям: {avg} руб.')

            elif choice == '4':
                higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
                print('Заработная плата выше средней: ')
                for company, salary, vacancy in higher_salary_vacancies:
                    print(f'Заработная плата выше среднего значения: Компания - {company}, Должность - {vacancy}, Заработная плата: {salary} руб.')

            elif choice == '5':
                keyword = input("Введите ключевое слово для поиска: ")
                with_keyword = db_manager.get_vacancies_with_keyword(keyword)
                print(f'Произведена выборка по ключевому слову: {keyword} ')
                for company, vacancy, link in with_keyword:
                    print(f'Вакансии по ключевому слову: {keyword}, {company},{vacancy},{link}')
            elif choice == '6':
                print("Программа завершена")
                break
            else:
                print("Некорректный ввод. Пожалуйста, попробуйте снова.")

    finally:
        db_manager.close_connection()


if __name__ == '__main__':
    db_name = 'project_vacancy'
    creating_bd(db_name)
    create_table(db_name)
    connect_api()
    user_managment()
