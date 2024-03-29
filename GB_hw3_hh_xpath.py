#   1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика с сайта job.ru или hh.ru.
#      (Можно с обоих сразу) Приложение должно анализировать несколько страниц сайта.
#      Получившийся список должен содержать в себе:
#           *Наименование вакансии,
#           *Предлагаемую зарплату
#           *Ссылку на саму вакансию
#   2) Доработать приложение таким образом, чтобы можно было искать разработчиков
#       на разные языки программирования (Например Python, Java, C++)
#
#
#


import requests
from lxml import html


def get_data_from_hh(get_data_from_hh_topic, number):
    print('/'*50)
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
        print('/'*50)
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
        for item in html.fromstring(text).xpath('''//a[@class="bloko-link HH-LinkModifier"]/text() |
                                           //a[@class="bloko-link HH-LinkModifier"]/@href |
                                           //*[contains(@class,"compensation")]/text()'''):
            if item.startswith('http'):
                counter += 1
                data_file.write('-'*25 + str(counter) + '-'*25 + '\n')
                print('-'*25 + str(counter) + '-'*25)
            data_file.write(item + '\n')
            print(item)
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
