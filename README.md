# Парсер для поиска вакансий на hh и habr.

Программа позволяет искать вакансии разработчика **Python** уровня **стажер** и **Junior** на сайтах [hh.ru](https://hh.ru/) и [career.habr.com](career.habr.com), добавлять их в базу и при последующем обновлении убирать неактивные предложения в архив. 

Новости с career.habr.com получаем с помощью парсинга страниц по заданным url.

Новости с hh.ru получаем по API с заданными параметрами вакансий. 

Все необходимые url добавляются в файл .env, в качестве примера сморите .env.template.

База данных - **PostgreSQL**. Работа с БД идет через **SQLAlchemy**.


## Установка.
Выполните в консоли:
```
git clone https://github.com/user-name-art/job_search.git

python3 -m venv env

source env/bin/activate

pip install -r requirments.txt
```

## Настройка.
Заполните .env файл по образцу .env.template.


## Запуск парсеров.
Парсеры могут работать по расписанию  с помощью Celery (по умолчанию запуск раз в сутки). Для запуска Celery выполните в консоли:
```
celery -A tasks worker -B --loglevel=INFO
```
Также можно запустить каждый парсер вручную:
```
python3 webapp/parsers/habr.py
python3 webapp/parsers/hh.py
```