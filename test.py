import pymongo
from config import *
# mongo --username Mongodbadmin --password Mongodbadmin --authenticationDatabase kindle_metadata --host 35.174.211.255 --port 27017
# init mongodb
# Search for existing book by author and by title.
mongodb = pymongo.MongoClient(f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_IP}/?authSource={MONGODB_COLLOC}&authMechanism=SCRAM-SHA-256")
mongodb_db = mongodb["kindle_metadata"]
mongodb_col = mongodb_db["kindle_metadata"]

for i in mongodb_col.find({'categories':{'$elemMatch':{'$elemMatch':{'$in':['Organic']}}}}):
    print(i)

