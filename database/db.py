from pymongo import MongoClient

class DB(object):

    def __init__(self):
        self.client = MongoClient()
        self.database = "kecilin_intern"

    def insertDB(self, data):
        db = self.client[self.database]
        collection = "twitter_data"
        return db[collection].insert_one(data)
