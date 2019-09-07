#   Beautiful soup example done in class
#   Searchin for job key word in HH.ru and output Title, Link, Salary onto screen
#

import requests
from bs4 import BeautifulSoup


def request_to_site():
    headers = {
        'accept': '*/*',
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5.0.342.5 Safari/533.2'
    }
    params = {
        'text': 'программист'
    }
    try:
        request = requests.get('https://hh.ru/search/vacancy', params=params, headers=headers)
        print("Request Status: ", request.status_code)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your internet connection')
        exit(1)


def parse_vacancies():
    html_doc = request_to_site()
    soup = BeautifulSoup(html_doc, 'html.parser')
    vacancies = soup.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'}, limit=10)
    print(len(vacancies), ' vacancies found')
    print('-*' * 50)
    for vacancy in vacancies:
        print(vacancy.find('a').string)
        print(vacancy.find('a')['href'])
        try:
            print(vacancy.find('div', {'class': 'vacancy-serp-item__compensation'}).string)
        except AttributeError:
            print('Salary not indicated')
        print('-*'*50)
    return 0


parse_vacancies()
