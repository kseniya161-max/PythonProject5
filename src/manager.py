import psycopg2
import config
from typing import List, Tuple, Optional
from bd import creating_bd


class DBManager:
    """Подключение к Базе данных"""
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        self.cursor = self.conn.cursor()

        # conn.autocommit = True
    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """ Получает список всех компаний и количество Вакансий у компаний"""
        query = """
        SELECT company.company_name,COUNT (company_vacancy.vacancy_id) AS vacancy_count
        FROM company
        LEFT JOIN company_vacancy ON company.company_id = company_vacancy.org_id
        GROUP BY company.company_name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, str, Optional[float]]]:
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        query = """
        SELECT company.company_name, company_vacancy.vacancy_name, company_vacancy.link, company_vacancy.salary
        FROM company_vacancy
        JOIN company ON company_vacancy.org_id = company.company_id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату"""
        query = """
        SELECT AVG(salary) FROM company_vacancy;"""
        self.cursor.execute(query)
        avg_salary = self.cursor.fetchone()[0]
        return round(avg_salary, 2) if avg_salary is not None else 0.0  # Округление до 2 знаков после запятой

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, Optional[float]]]:
        """получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        query = """
        SELECT company.company_name, company_vacancy.vacancy_name, company_vacancy.salary
        FROM company_vacancy 
        JOIN company  ON company_vacancy.org_id = company.company_id
        WHERE company_vacancy.salary > %s;"""
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, str]]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
 например python."""
        query = """
               SELECT company.company_name, company_vacancy.vacancy_name, company_vacancy.link
               FROM company_vacancy 
               JOIN company  ON company_vacancy.org_id = company.company_id
               WHERE company_vacancy.vacancy_name ILIKE %s;
               """
        self.cursor.execute(query, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def close_connection(self) -> None:
        """Закрываем соединение"""
        self.cursor.close()
        self.conn.close()


# if __name__ == "__main__":
#     db_manager = DBManager()
#     try:
#         companies_count = db_manager.get_companies_and_vacancies_count()
#         print(companies_count)
#
#         all_vacancies = db_manager.get_all_vacancies()
#         print(all_vacancies)
#
#         avg_salary = db_manager.get_avg_salary()
#         print(f"Средняя зарплата по всем вакансиям: {avg_salary}")
#
#         higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
#         print(higher_salary_vacancies)
#
#         keyword_vacancies = db_manager.get_vacancies_with_keyword("Junior")
#         print(f'Компании по ключевому слову: {keyword_vacancies}')
#     finally:
#         db_manager.close_connection()
