import os
import sys
sys.path.append(os.getcwd())

from flask import Flask, render_template

from webapp.models import Vacancy


def create_app():
    app = Flask((__name__))

    @app.route('/')
    def index():
        title = 'Вакансии python.'
        active_vacancies = Vacancy.query.filter(Vacancy.active == True).order_by(Vacancy.published.desc()).all()
        archive_vacancies = Vacancy.query.filter(Vacancy.active == False).order_by(Vacancy.published.desc()).all()
        return render_template('index.html', page_title=title,
                               active_vacancies=active_vacancies,
                               archive_vacancies=archive_vacancies)

    return app
