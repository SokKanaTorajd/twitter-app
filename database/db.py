from pymongo import MongoClient

class DB(object):

    def __init__(self, db, URI=None):
        
        # Atlas Connection
        if URI is not None:
            self.client = MongoClient(URI)
        
        # localhost connection
        if URI is None:
            self.client = MongoClient()

        self.database = db
    
    def setDBConnection(self):
        return self.client[self.database]

    def checkExistedDoc(self, collection, key, value):
        db = self.setDBConnection()
        result = db[collection].find_one({key: value})
        if result is None:
            existed = False
        else:
            existed = True
        return existed
    
    def updateDataByOne(self, collection, old_data, new_data):
        db = self.setDBConnection()
        return db[collection].update_one(old_data, new_data)

    def insertDataByOne(self, collection, data):
        db = self.setDBConnection()
        return db[collection].insert_one(data)
    
    def getDataByOne(self, collection, key, value):
        db = self.setDBConnection()
        result = db[collection].find_one({key: value})
        return result

