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
        all_vacancies = Vacancy.query.order_by(Vacancy.published.desc()).all()
        return render_template('index.html', page_title=title, all_vacancies=all_vacancies)

    return app
