import os
import sys
sys.path.append(os.getcwd())

import requests

from dotenv import load_dotenv

from webapp.models import Vacancy
from webapp.db import db_session


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException):
        print('Network error.')
        return False

def save_data_to_db(all_vacancies):
    for vacancy in all_vacancies:
        vacancy_exists = Vacancy.query.filter(Vacancy.url == vacancy['url']).count()
        
        if not vacancy_exists:
            entity = Vacancy(company=vacancy['company'], vacancy_title=vacancy['vacancy_title'], 
                        url=vacancy['url'], published=vacancy['published'])
            db_session.add(entity)
            db_session.commit()
            print(f"Вакансия {vacancy['vacancy_title']} компании {vacancy['company']} добавлена.")
        else:
            print(f"Вакансия {vacancy['vacancy_title']} компании {vacancy['company']} уже есть в базе.")