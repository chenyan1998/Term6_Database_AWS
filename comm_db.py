from fastapi import FastAPI
from sqlalchemy import Column, VARCHAR, TEXT, INTEGER,CHAR, create_engine,func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql.sqltypes import INT
import pymongo
from config import *


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
    reviewText = Column(VARCHAR(8000))
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
session = DBSession()
# # get CURRENT_REVIEW_IDX from mysql
# CURRENT_REVIEW_IDX = session.query(func.max(Review.idx)).scalar() with autoincrement, dont need this


# init mongodb
# Search for existing book by author and by title.
mongodb = pymongo.MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_IP}/?authSource={MONGODB_COLLOC}&authMechanism=SCRAM-SHA-256")
mongodb_db = mongodb["kindle_metadata"]
mongodb_col = mongodb_db["kindle_metadata"]

# review = session.query(Review).filter(Review.id==6).one()
# print(review.summary)

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def mongo_fetch_all(cur):
    result = []
    for i in cur:
        result.append(i)
    return result

@app.get("/readreview/")
def read_review(asin: str='', reviewerID:str=''):
    if asin and reviewerID:
        reviews = session.query(Review).filter(Review.asin == asin).filter(Review.reviewerID == reviewerID).all()
    elif asin:
        reviews = session.query(Review).filter(Review.asin == asin).all()
    else:
        reviews = session.query(Review).filter(Review.reviewerID == reviewerID).all()
    return reviews

@app.get("/addreview/")
def add_review(asin: str='', reviewerID:str='',content:str=''):
    # global CURRENT_REVIEW_IDX
    # CURRENT_REVIEW_IDX += 1
    new_review = Review(asin=asin,reviewText=content)
    session.add(new_review)
    session.flush()
    session.commit()
    return {'success':True}

@app.get('/readbook/')
def read_book(author:str='',title:str=''):
    if author and title:
        result = mongo_fetch_all(mongodb_col.find({'author':f'/{author}/','title':f'/{title}/'},{'_id':0}))
    elif author:
        result = mongo_fetch_all(mongodb_col.find({'author':f'/{author}/'},{'_id':0}))
    else:
        result = mongo_fetch_all(mongodb_col.find({'title':{'$regex': f".*{title}.*", '$options': 'i'}},{'_id':0}))
    return result

@app.get('/addbook/')
def add_book(author:str='',title:str='',asin:str='',description:str='',imUrl:str='',price:str=''):
    mongodb_col.insert({'title':title,'asin':asin,'description':description,'imUrl':imUrl,'price':price})
    return {'success':True}

