from pymongo import MongoClient
import os

class DB(object):

    def __init__(self):
        # self.client = MongoClient()
        self.client = MongoClient(os.environ.get('MONGODB_URI'))
        self.database = "kecilin-intern"

    def insertAuthorizedUser(self, data):
        db = self.client[self.database]
        collection = "twitter-app"
        return db[collection].insert_one(data)
    
    def getUserAccess(self, id):
        db = self.client[self.database]
        collection = "twitter-app"
        result = db[collection].find_one('user_id': id)
        return result['access']

    def insertTweet(self, data):
        db = self.client[self.database]
        collection = "twitter-data"
        return db[collection].insert_one(data)
