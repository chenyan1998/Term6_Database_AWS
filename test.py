import pymongo
# mongo --username Mongodbadmin --password Mongodbadmin --authenticationDatabase kindle_metadata --host 35.174.211.255 --port 27017
mongodb = pymongo.MongoClient("mongodb://Mongodbadmin:Mongodbadmin@35.174.211.255/?authSource=kindle_metadata&authMechanism=SCRAM-SHA-256")
mongodb_db = mongodb["kindle_metadata"]
mongodb_col = mongodb_db["kindle_metadata"]

# for x in mycol.find({},{ "_id": 0, "name": 1, "alexa": 1 }):
#   print(x)

for i in mongodb_col.find({'title':{'$regex': ".*power.*", '$options': 'i'}}):
    print(i)

