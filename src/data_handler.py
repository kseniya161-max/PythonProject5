import psycopg2
from psycopg2 import sql
import config

def filling_company(cursor,company_name):
    """Вставка компании в таблицу Компании"""
    cursor.execute(
        "INSERT INTO company (company_name) VALUES (%s) ON CONFLICT (company_name) DO NOTHING;",
        (company_name,)
    )

def filling_company_vacancy(cursor, company_name, vacancy):
    """Вставка Вакансии в таблицу Вакансии"""
    vacancy_name = vacancy['name']
    link = vacancy['alternate_url']
    cursor.execute("""
        INSERT INTO company_vacancy (vacancy_name, org_id, link)
         VALUES (%s, (SELECT company_id FROM company WHERE company_name = %s),%s);""", (vacancy_name,company_name, link)

    )
