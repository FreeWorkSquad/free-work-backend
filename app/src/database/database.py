from pymongo.database import Database
from app.src.database.collection import Collection


def __encode__(data):  # JSON 안의 데이터가 ObjectId 타입인 경우 문자열로 변환
    if data is None:
        return None
    if '_id' in data:
        data['_id'] = str(data['_id'])
    return data


class Database:
    def __init__(self, db: Database):
        self.db = db

    def insert_one(self, collection: Collection, data):
        inserted_id = self.db[collection.value].insert_one(data).inserted_id
        return str(inserted_id)

    def find(self, collection: Collection, query):
        return self.db[collection.value].find(query)

    def find_all(self, collection: Collection):
        for document in self.db[collection.value].find():
            yield __encode__(document)

    def find_one(self, collection: Collection, query):
        return __encode__(self.db[collection.value].find_one(query))

    def update_one(self, collection: Collection, query, new_data):
        modified_count = self.db[collection.value].update_one(query, {'$set': new_data}).modified_count
        return str(modified_count)

    def delete_one(self, collection: Collection, query):
        return self.db[collection.value].delete_one(query).deleted_count

    def delete_many(self, collection: Collection, query):
        return __encode__(self.db[collection.value].delete_many(query).raw_result)

    def is_exist(self, collection: Collection, query):
        return self.find_one(collection=collection, query=query) is not None

    def is_not_exist(self, collection: Collection, query):
        return not self.is_exist(collection=collection, query=query)
