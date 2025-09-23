import requests
import json

def connect_api():
    """ Подключение API"""
    employer_ids = [
        9694561,
        2180,
        78638,
        2748, # Ростелеком
        1388900, #Сбертех
        1057, # Лаборатория Касперского
        15478, # VK
        6093775, # Астон Стажировка
        125419124, # МТС IT
        41862 # Контур
    ]    #  по id работодателей которые меня интересуют
    for emp_id in employer_ids:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={emp_id}')

        if response.status_code == 200:
            vacancies = response.json().get('items',[])
            print(f"Вакансии по этому ID Работодателю {emp_id}:")

            if vacancies:
                for vacancy in vacancies:
                    print(f"- {vacancy['name']} (URL: {vacancy['alternate_url']})")

            else:
                print('Нет открытых Вакансий')
        else:
            print(f'Ошибка при получении данных с этого ID Работодателя {emp_id} {response.status_code}')

connect_api()
