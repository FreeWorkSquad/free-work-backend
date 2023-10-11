from pymongo.database import Database
from app.src.database.collection import Collection


class Database:
    def __init__(self, db: Database):
        self.db = db

    def insert_one(self, collection: Collection, data):
        return self.db[collection.value].insert_one(data)

    def find(self, collection: Collection, query):
        return self.db[collection.value].find(query)

    def find_all(self, collection: Collection):
        for document in self.db[collection.value].find():
            yield document

    def find_one(self, collection: Collection, query):
        return self.db[collection.value].find_one(query)

    def update_one(self, collection: Collection, query, data):
        return self.db[collection.value].update_one(query, data)

    def delete_one(self, collection: Collection, query):
        return self.db[collection.value].delete_one(query)

    def delete_many(self, collection: Collection, query):
        return self.db[collection.value].delete_many(query)