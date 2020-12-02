from fastapi import FastAPI
from sqlalchemy import Column, VARCHAR, TEXT, INTEGER,CHAR, create_engine,func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.sqltypes import INT
import pymongo
from config import *
from urllib.parse import unquote
import logging

Base = declarative_base()
# define a Review object
class Review(Base):
    # table name
    __tablename__ = MYSQL_TABLE
    # structure
    idx = Column(INT, primary_key=True)
    asin = Column(CHAR(10))
    helpful = Column(TEXT)
    overall = Column(INT)
    review = Column(VARCHAR(8000))
    reviewTime = Column(TEXT)
    reviewerID = Column(TEXT)
    reviewerName = Column(TEXT)
    summary = Column(TEXT)
    unixReviewTime = Column(TEXT)


# CURRENT_REVIEW_IDX = 0
# init mysql connection
# engine = create_engine('mysql+pymysql://root:jrKa2qZhpt-Easd3GGV97@localhost:3306/kindle_review')
engine = create_engine(f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_IP}:{MYSQL_PORT}/{MYSQL_DATABASE}')
DBSession = sessionmaker(bind=engine)
# session = DBSession()
# # get CURRENT_REVIEW_IDX from mysql
# CURRENT_REVIEW_IDX = session.query(func.max(Review.idx)).scalar() with autoincrement, dont need this


# init mongodb
# Search for existing book by author and by title.
mongodb = pymongo.MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_IP}/?authSource={MONGODB_COLLOC}&authMechanism=SCRAM-SHA-256")
mongodb_db = mongodb["kindle_metadata"]
mongodb_col = mongodb_db["kindle_metadata"]

# review = session.query(Review).filter(Review.id==6).one()
# print(review.summary)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def mongo_fetch_all(cur):
    result = []
    result.append(cur.count())
    for i in cur:
        result.append(i)
    return result

@app.get("/readreview/")
def read_review(asin: str='', reviewerID:str=''):
    session = DBSession()
    if asin and reviewerID:
        reviews = session.query(Review).filter(Review.asin == asin).filter(Review.reviewerID == reviewerID).all()
    elif asin:
        reviews = session.query(Review).filter(Review.asin == asin).all()
    else:
        reviews = session.query(Review).filter(Review.reviewerID == reviewerID).all()
    session.close()
    return reviews

@app.get("/addreview/")
def add_review(asin: str='', reviewerID:str='',content:str=''):
    # global CURRENT_REVIEW_IDX
    # CURRENT_REVIEW_IDX += 1
    session = DBSession()
    new_review = Review(asin=asin,review=content)
    session.add(new_review)
    session.flush()
    session.commit()
    session.close()
    return {'success':True}

@app.get('/readbook/')
def read_book(author:str='',title:str='',category='',offset:int=0,batch=50):
    if author and title:
        result = mongo_fetch_all(mongodb_col.find({'author':f'/{author}/','title':f'/{title}/'},{'_id':0},skip=offset,limit=batch))
    elif author:
        result = mongo_fetch_all(mongodb_col.find({'author':f'/{author}/'},{'_id':0},skip=offset,limit=batch))
    elif category:
        category = unquote(category)
        result = mongo_fetch_all(mongodb_col.find({'categories':{'$elemMatch':{'$elemMatch':{'$in':[f'{category}']}}}},{'_id':0},skip=offset,limit=batch))
    else:
        result = mongo_fetch_all(mongodb_col.find({'title':{'$regex': f".*{title}.*", '$options': 'i'}},{'_id':0},skip=offset,limit=batch))
    return result

@app.get('/addbook/')
def add_book(author:str='',title:str='',asin:str='',description:str='',imUrl:str='',price:str=''):
    mongodb_col.insert({'title':title,'asin':asin,'description':description,'imUrl':imUrl,'price':price})
    return {'success':True}

