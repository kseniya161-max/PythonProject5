import requests
from data_handler import filling_company, filling_company_vacancy
from src import config
import psycopg2


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
    conn = psycopg2.connect(
        dbname='project_vacancy',
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()  # Открываем курсор

    for emp_id in employer_ids:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={emp_id}', headers=headers)

        if response.status_code == 200:
            vacancies = response.json().get('items', [])
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
                print('Нет открытых Вакансий')
        else:
            print(f'Ошибка при получении данных с этого ID Работодателя {emp_id} {response.status_code}')
    cursor.close()
    conn.close()


if __name__ == '__main__':
    connect_api()
