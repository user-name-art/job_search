from sqlalchemy import Column, Integer, String, Date
from db import Base, engine


class Vacancy(Base):
    __tablename__ = 'vacancies'

    id = Column(Integer, primary_key=True)
    company = Column(String)
    vacancy_title = Column(String)
    url = Column(String)
    published = Column(Date)

    def __repr__(self):
        return f'Vacancy {self.id}, {self.company}, {self.vacancy_title}'

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)