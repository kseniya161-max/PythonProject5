import requests
import json

def connect_api():
    employer_ids = [
        9694561,
        2180,
        78638
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


    # url_base = "https://api.hh.ru/"
    #
    # status_code = response.status_code
