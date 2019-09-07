#    This code is based on teacher's ways to search in HH.ru for jobs
#    It is using xpath
#    Prints data onto screen and into a file

import requests
from lxml import html


def get_data_from_hh(get_data_from_hh_topic, number):
    print('/' * 50)
    print('page #', str(int(number) + 1))
    params = {
        'only_with_salary': 'false',
        'clusters': 'true',
        'enable_snippents': 'true',
        'salary': '',
        'st': 'searchVacancy',
        'text': get_data_from_hh_topic,
        'page': number,
    }
    res: str = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.2 ' \
               '(KHTML, like Gecko) Chrome/5.0.342.5 Safari/533.2'
    try:
        response = requests.get('https://hh.kz/search/vacancy?', params=params, headers={'User-Agent': res})
        print('RESPONSE STATUS:', response.status_code)
        print('/' * 50)
        text: str = response.content.decode('utf-8')
        return text
    except requests.exceptions.ConnectionError:
        print("Check your internet connection")
        exit(1)


def get_page_data(text, number, p_counter):
    counter = 20 * p_counter
    if number == 0:
        file_open_mode = 'w'
    else:
        file_open_mode = 'a'
    with open('hh_data.txt', file_open_mode) as data_file:
        if p_counter == 0:
            vacancies = str(html.fromstring(text).xpath("//h1[@class='header']/text()")).replace(u'\\xa0', u' ')
            print(vacancies[2:-2])
            data_file.write(vacancies + '\n')
        all_vacancies = html.fromstring(text).xpath('//div[div[contains(@class,"item__row_header")]]')
        for item in all_vacancies:
            data_file.write('-' * 25 + str(counter + 1) + '-' * 25 + '\n')
            print('-' * 25 + str(counter + 1 ) + '-' * 25)
            search_element = item.xpath('//a[@class="bloko-link HH-LinkModifier"]/text()')[0]
            print(search_element)
            data_file.write(search_element +'\n')
            search_element = item.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href')[0]
            print(search_element)
            data_file.write(search_element +'\n')
            try:
                search_element = item.xpath('//*[contains(@class,"compensation")]/text()')[0]
                print(search_element)
                data_file.write(search_element +'\n')
            except IndexError:
                print('Salary not indicated')
                data_file.write('Salary not indicated')
            counter += 1

    return 0


def get_data(get_data_topic, max_pages):
    """

    :param get_data_topic: - search keyword
    :type max_pages: integer - needed to limit the search
    """
    page_counter = 0
    text = get_data_from_hh(get_data_topic, page_counter)
    get_page_data(text, page_counter, page_counter)
    next_button = html.fromstring(text).xpath('//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]')
    while next_button != '' and page_counter < max_pages:
        page_counter += 1
        text = get_data_from_hh(get_data_topic, page_counter)
        get_page_data(text, page_counter, page_counter)
        next_button = html.fromstring(text).xpath('//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]')
    return 0


topic = input('Please enter your search topic:').rstrip()
number_of_pages = int(input('Please enter number of pages to display:').rstrip())
get_data(topic, number_of_pages - 1)
