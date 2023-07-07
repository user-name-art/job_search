import requests
import time
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy.exc import PendingRollbackError, IntegrityError

from models import Vacancy
from db import db_session


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error.')
        return False


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
            'published': published
        })  
    
    return result_vacancies


def save_data_to_db(all_vacancies):
    for vacancy in all_vacancies:
        try:
            entity = Vacancy(company=vacancy['company'], vacancy_title=vacancy['vacancy_title'], 
                        url=vacancy['url'], published=vacancy['published'])
            db_session.add(entity)
            db_session.commit()
            print(vacancy)
        except (PendingRollbackError, IntegrityError):
            print(f"Вакансия {vacancy['company']} {vacancy['vacancy_title']} уже есть в базе.")
    

if __name__ == '__main__':
    load_dotenv()
    habr_url = os.environ.get('HABR_URL')
    html = get_html(habr_url)
    if html:
        vacancies = get_habr_vacancies(html)
        save_data_to_db(vacancies)
        