import os
import sys
sys.path.append(os.getcwd())

from sqlalchemy import Column, Integer, String, Date, Boolean
from webapp.db import Base, engine


class Vacancy(Base):
    __tablename__ = 'vacancies'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    company = Column(String)
    vacancy_title = Column(String)
    url = Column(String, unique=True)
    published = Column(Date)
    active = Column(Boolean)
    source = Column(String)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}, {self.company}, {self.vacancy_title})'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
