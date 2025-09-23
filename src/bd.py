import psycopg2
from psycopg2 import sql

def creating_bd(db_name):
    """ Создание Базы данных и подключение"""
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True #создаем автокомит

    cursor = conn.cursor()
    cursor.execute(sql.SQL("CREATE DATABASE {}").format (sql.Identifier(db_name)))
    print(f'База данных {db_name} успешно создана ')

    cursor.close()
    conn.close()


if __name__ == "__main__":
    creating_bd('project_vacancy')