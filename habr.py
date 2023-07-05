import requests
from bs4 import BeautifulSoup


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
        published = vacancy.find('time').text
        
        result_vacancies.append({
            'company': company,
            'title': title,
            'url': url,
            'published': published
        })  
    
    return result_vacancies


if __name__ == '__main__':
    html = get_html('https://career.habr.com/vacancies?qid=3&s[]=2&s[]=82&s[]=72&s[]=1&s[]=106&skills[]=446&type=all')
    if html:
        vacancies = get_habr_vacancies(html)
        print(vacancies)
