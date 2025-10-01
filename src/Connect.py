import requests
from data_handler import filling_company, filling_company_vacancy
from src import config
import psycopg2


# def connect_api():
#     """ Подключение API"""
#     employer_ids = [
#         9694561,
#         2180,
#         78638,
#         2748,   # Ростелеком
#         1388900,   # Сбертех
#         1057,   # Лаборатория Касперского
#         15478,   # VK
#         6093775,   # Астон Стажировка
#         125419124,   # МТС IT
#         41862   # Контур
#     ]
#
#     headers = {
#         'User-Agent': 'My_pr/1.0 (baharavaxen@yandex.ru)',
#     }
#     conn = psycopg2.connect(
#         dbname='project_vacancy',
#         user=config.DB_USER,
#         password=config.DB_PASSWORD,
#         host=config.DB_HOST,
#         port=config.DB_PORT
#     )
#     conn.autocommit = True
#     cursor = conn.cursor()  # Открываем курсор
#
#     for emp_id in employer_ids:
#         response = requests.get(f'https://api.hh.ru/vacancies?employer_id={emp_id}', headers=headers)
#
#         if response.status_code == 200:
#             vacancies = response.json().get('items', [])
#             print(f"Вакансии по этому ID Работодателю {emp_id}:")
#
#             if vacancies:
#                 company_name = vacancies[0].get('employer', {}).get('name', 'Неизвестно')
#                 filling_company(cursor, company_name)
#
#                 for vacancy in vacancies:
#                     salary = vacancy.get('salary')
#                     if salary is not None:
#                         salary_value = salary.get('from', 0)
#                     else:
#                         salary_value = 0
#
#                     print(f"- {vacancy['name']} (URL: {vacancy['alternate_url']}),Salary: {salary_value}")
#                     filling_company_vacancy(cursor, company_name, vacancy, salary_value)
#
#             else:
#                 print('Нет открытых Вакансий')
#         else:
#             print(f'Ошибка при получении данных с этого ID Работодателя {emp_id} {response.status_code}')
#     cursor.close()
#     conn.close()
#
#
# if __name__ == '__main__':
#     connect_api()

def get_vacancies_from_api(emp_id):
    """Получение вакансий с апи адреса по id"""
    headers = {
        'User-Agent': 'My_pr/1.0 (baharavaxen@yandex.ru)',
    }

    response = requests.get(f'https://api.hh.ru/vacancies?employer_id={emp_id}', headers=headers)
    if response.status_code == 200:
        return response.json().get('items', [])

    else:
        print(f'Ошибка при получении данных с этого ID Работодателя {emp_id}: {response.status_code}')
        return []

def connect_to_database():
    """Подключаемся к базе данных"""
    conn = psycopg2.connect(
        dbname=config.DB_NAME, # Исправила чтобы подключаться неявно а из файла config
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    conn.autocommit = True
    # cursor = conn.cursor()  # Открываем курсор
    return conn


def processing_vacancies(employer_ids,cursor):
    """Обработка Вакансий из списка работодателей"""
    for emp_id in employer_ids:
        vacancies = get_vacancies_from_api(emp_id)
        print(f"Вакансии по этому ID Работодателю {emp_id}:")
        if vacancies:
            company_name = vacancies[0].get('employer', {}).get('name', 'Неизвестно')
            filling_company(cursor, company_name)

            for vacancy in vacancies:
                salary = vacancy.get('salary')
                if salary is not None:
                    salary_value = salary.get('from', 0)
                else:
                    salary_value = 0

                print(f"- {vacancy['name']} (URL: {vacancy['alternate_url']}),Salary: {salary_value}")
                filling_company_vacancy(cursor, company_name, vacancy, salary_value)

        else:
            print(f'Нет открытых Вакансий по данному ID {emp_id}')
        # else:
        #     print(f'Ошибка при получении данных с этого ID Работодателя {emp_id} {response.status_code}')

def connect_api():
    """ Подключение API"""
    employer_ids = [
        9694561,
        2180,
        78638,
        2748,   # Ростелеком
        1388900,   # Сбертех
        1057,   # Лаборатория Касперского
        15478,   # VK
        6093775,   # Астон Стажировка
        125419124,   # МТС IT
        41862   # Контур
    ]

    headers = {
        'User-Agent': 'My_pr/1.0 (baharavaxen@yandex.ru)',
    }
    conn = connect_to_database()
    cursor = conn.cursor()
    processing_vacancies(employer_ids, cursor)
    cursor.close()
    conn.close()



if __name__ == '__main__':
    connect_api()