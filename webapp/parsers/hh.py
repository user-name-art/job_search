import os
import sys

from dotenv import load_dotenv

import requests

sys.path.append(os.getcwd())

from webapp.parsers.utils import save_data_to_db, switch_active


def get_data(source_url):
    try:
        response = requests.get(source_url, params=None)
        all_vacancies = response.json()['items']
    except (requests.RequestException):
        print('Network error.')
        return False

    result_vacancies = []

    for vacancy in all_vacancies:
        company = vacancy['employer']['name']
        title = vacancy['name']
        url = vacancy['alternate_url']
        published = vacancy['published_at'].split('T')[0]

        result_vacancies.append({
            'company': company,
            'vacancy_title': title,
            'url': url,
            'published': published,
            'source_url': 'hh',
        })

    save_data_to_db(result_vacancies)

    return result_vacancies


if __name__ == '__main__':
    load_dotenv()

    switch_active('hh')

    hh_url_intern = os.environ.get('HH_URL_INTERN')
    get_data(hh_url_intern)

    hh_url_junior = os.environ.get('HH_URL_JUNIOR')
    get_data(hh_url_junior)

    hh_url_kazan_intern = os.environ.get('HH_URL_KAZAN_INTERN')
    get_data(hh_url_kazan_intern)

    hh_url_kazan_junior = os.environ.get('HH_URL_KAZAN_JUNIOR')
    get_data(hh_url_kazan_junior)
