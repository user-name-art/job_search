from bs4 import BeautifulSoup
from dotenv import load_dotenv

import os
import sys
sys.path.append(os.getcwd())

from webapp.parsers.utils import save_data_to_db, get_html, switch_active


def get_habr_vacancies(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_vacancies = soup.find('div', class_='section-group section-group--gap-medium')
    all_vacancies = all_vacancies.findAll('div', class_='vacancy-card__inner')

    result_vacancies = []
    for vacancy in all_vacancies:
        company = vacancy.find('div', 'vacancy-card__company-title').find('a').text
        title = vacancy.find('a', class_='vacancy-card__title-link').text
        url = f"https://career.habr.com{vacancy.find('a', class_='vacancy-card__title-link')['href']}"
        published = vacancy.find('time')['datetime'].split('T')[0]

        result_vacancies.append({
            'company': company,
            'vacancy_title': title,
            'url': url,
            'published': published,
            'source_url': 'habr',
        })

    save_data_to_db(result_vacancies)

    return result_vacancies


if __name__ == '__main__':
    load_dotenv()

    switch_active('habr')

    habr_url_junior = os.environ.get('HABR_URL_JUNIOR')
    habr_url_intern = os.environ.get('HABR_URL_INTERN')

    html = get_html(habr_url_junior)
    if html:
        vacancies = get_habr_vacancies(html)

    html = get_html(habr_url_intern)
    if html:
        vacancies = get_habr_vacancies(html)
