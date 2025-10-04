import psycopg2
from psycopg2 import sql
import config


def creating_bd(db_name):
    """ Создание Базы данных и подключение"""
    conn = psycopg2.connect(
        dbname='postgres',
        user=config.DB_USER,
        password=config.DB_PASSWORD ,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    conn.autocommit = True    # создаем автокомит

    cursor = conn.cursor()   # Открываем курсор
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f'База данных {db_name} успешно создана ')

    cursor.close()
    conn.close()


def create_table(db_name):
    """Создание Таблицы в БД"""
    conn = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    conn.autocommit = True

    cursor = conn.cursor()   # Открываем курсор
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company(
        company_id SERIAL PRIMARY KEY,
        company_name VARCHAR (200) NOT NULL UNIQUE
    );""")

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_vacancy(
            vacancy_id SERIAL PRIMARY KEY,
            vacancy_name VARCHAR (100) NOT NULL,
            org_id INTEGER NOT NULL,
            link VARCHAR (100) NOT NULL,
            salary NUMERIC,
            FOREIGN KEY (org_id) REFERENCES company(company_id)
        );""")
    print("Таблицы успешно созданы")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    db_name = 'project_vacancy'
    creating_bd(db_name)
    create_table(db_name)
