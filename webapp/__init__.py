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
        return render_template('index.html', page_title=title)

    return app
