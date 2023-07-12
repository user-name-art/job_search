import os

from celery import Celery
from celery.schedules import crontab

from webapp.parsers.utils import switch_active, get_html
from webapp.parsers.habr import get_habr_vacancies
from webapp.parsers.hh import get_data


celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def habr_vacancies():
    switch_active('habr')

    habr_url_junior = os.environ.get('HABR_URL_JUNIOR')
    html = get_html(habr_url_junior)
    if html:
        vacancies = get_habr_vacancies(html)

    habr_url_intern = os.environ.get('HABR_URL_INTERN')
    html = get_html(habr_url_intern)
    if html:
        vacancies = get_habr_vacancies(html)


@celery_app.task
def hh_vacancies():
    switch_active('hh')

    hh_url_intern = os.environ.get('HH_URL_INTERN')
    get_data(hh_url_intern)

    hh_url_junior = os.environ.get('HH_URL_JUNIOR')
    get_data(hh_url_junior)

    hh_url_kazan_intern = os.environ.get('HH_URL_KAZAN_INTERN')
    get_data(hh_url_kazan_intern)

    hh_url_kazan_junior = os.environ.get('HH_URL_KAZAN_JUNIOR')
    get_data(hh_url_kazan_junior)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=0, hour=4), habr_vacancies.s())
    sender.add_periodic_task(crontab(minute=0, hour=4), hh_vacancies.s())