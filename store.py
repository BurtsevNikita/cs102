from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, String, Integer
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

from sqlalchemy import create_engine
engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
s = session()


def read_all():
    return s.query(News).all()

def read_unlabeled():
    return s.query(News).filter(News.label == None).all()


def insert_articles(articles, break_at_first_match = True):
    for row in articles:
        if s.query(News).filter(News.title == row['title'], News.author == row['author']).one_or_none():
            # find it
            if break_at_first_match:
                break
        else:
            s.add(News(**row))
    s.commit()

def update_label(news_id, label):
    row = s.query(News).filter(News.id == news_id).one_or_none()
    if row:
        row.label = label
        s.commit()