import requests

from webapp.models import Vacancy
from webapp.db import db_session


def get_html(url):
    """Функция получает html веб-страницы с указанным url.
    """
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException):
        print('Network error.')
        return False


def save_data_to_db(all_vacancies):
    """Функция сохраняет полученные данные в подключенную к сервису БД.
    Все новые вакансии по умолчанию помечаются как активные.
    Если вакансия ранее уже была добавлена в базу и она есть в полученном запросе,
    она также помечается как активная.
    На входе all_vacancies - это список словарей.
    """
    for vacancy in all_vacancies:
        vacancy_exists = Vacancy.query.filter(Vacancy.url == vacancy['url']).count()

        if not vacancy_exists:
            entity = Vacancy(company=vacancy['company'],
                             vacancy_title=vacancy['vacancy_title'],
                             url=vacancy['url'],
                             published=vacancy['published'],
                             active=True, source=vacancy['source_url'],
                             )
            db_session.add(entity)
            print(f"Вакансия {vacancy['vacancy_title']} {vacancy['company']} добавлена.")
        else:
            vacancy_by_url = Vacancy.query.filter(Vacancy.url == vacancy['url']).first()
            vacancy_by_url.active = True
            print(f"Вакансия {vacancy['vacancy_title']} {vacancy['company']} уже есть в базе.")

        db_session.commit()


def switch_active(source_url):
    """Переключает значение активности вакансии в False.
    Запускается каджый раз перед получением новых данных, чтобы пометить неактивные вакансии.
    """
    vacancies_by_source = Vacancy.query.filter(Vacancy.source == source_url).all()
    for vacancy in vacancies_by_source:
        vacancy.active = False
    db_session.commit()
