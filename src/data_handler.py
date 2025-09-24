import psycopg2
from psycopg2 import sql
import config


def filling_company(cursor, company_name):
    """Вставка компании в таблицу Компании"""
    try:
        cursor.execute(
            "INSERT INTO company (company_name) VALUES (%s) ON CONFLICT (company_name) DO NOTHING;",
            (company_name,)
        )
        print(f"Компания '{company_name}' добавлена.")
    except Exception as e:
        print(f"Ошибка при добавлении компании '{company_name}': {e}")


def filling_company_vacancy(cursor, company_name, vacancy, salary_value):
    """Вставка Вакансии в таблицу Вакансии"""
    try:
        vacancy_name = vacancy['name']
        link = vacancy['alternate_url']
        cursor.execute("""
            INSERT INTO company_vacancy (vacancy_name, org_id, link, salary)
            VALUES (%s, (SELECT company_id FROM company WHERE company_name = %s), %s, %s);""", (vacancy_name, company_name, link, salary_value)
                        )
        print(f"Вакансия '{vacancy_name}' добавлена.")
    except Exception as e:
        print(f"Ошибка при добавлении вакансии '{vacancy_name}': {e}")
