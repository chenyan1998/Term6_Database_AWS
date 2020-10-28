from fastapi import FastAPI
from sqlalchemy import Column, VARCHAR, TEXT, INTEGER, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware


Base = declarative_base()

# define a Review object
class Review(Base):
    # table name
    __tablename__ = 'review'
   # structure
    id = Column(INTEGER, primary_key=True)
    asin = Column(VARCHAR(100))
    helpful = Column(VARCHAR(100))
    overall = Column(INTEGER)
    reviewText = Column(TEXT)
    reviewTime = Column(VARCHAR(100))
    reviewerID = Column(VARCHAR(100))
    reviewName = Column(VARCHAR(100))
    summary = Column(TEXT)
    unixReviewTime = Column(VARCHAR(100))


# init mysql connection
engine = create_engine('mysql+pymysql://root:jrKa2qZhpt-Easd3GGV97@localhost:3306/kindle_review')
DBSession = sessionmaker(bind=engine)
session = DBSession()

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

@app.get("/review/")
def read_review(asin: str='', reviewerID:str=''):
    if asin and reviewerID:
        reviews = session.query(Review).filter(Review.asin == asin).filter(Review.reviewerID == reviewerID).all()
    elif asin:
        reviews = session.query(Review).filter(Review.asin == asin).all()
    else:
        reviews = session.query(Review).filter(Review.reviewerID == reviewerID).all()
    return reviews

