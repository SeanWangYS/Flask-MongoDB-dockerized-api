from pymongo import MongoClient
from bson.objectid import ObjectId
import logging

class MongoAPI:
    def __init__(self):
        # self.clinet = MongoClient("mongodb://localhost:27017/")   # When only Mongo DB is running on Docker.
        self.clinet = MongoClient("mongodb://mongodb:27017/")   # When both Mongo and This applicatio is running on
                                                                    # Docker and we are using Docker Compose
        database = self.clinet['database591']
        self.collection = database.houses

    def read(self, data):
        logging.info('search houses by filter')
        documents = self.collection.find(data['query'], data['projection'])
        documents = [doc for doc in documents]
        if '_id' in documents[0]:
            for doc in documents: doc['_id'] = str(doc['_id'])
        return documents

    def create(self, data):
        logging.info('create data')
        new_document = data['document']
        response = self.collection.insert_one(new_document)
        return {'status': 'successfully inserted', 
                'document_id': str(response.inserted_id)}

    def update(self, data):
        logging.info('update data') 
        query =  data['query']
        if "_id" in query:
            query['_id'] = ObjectId(query['_id'])
        update_data ={"$set": data['update_data']}
        response = self.collection.update_one(query, update_data)
        return {'status': 'successfully updated' if response.modified_count > 0 else "nothing to update."}
    
    def delete(self, data):
        logging.info('delete data')
        query =  data['query']
        if "_id" in query:
            query['_id'] = ObjectId(query['_id'])
        response = self.collection.delete_one(query) # supposed to delete by "_id"
        return {'status': 'successfully deleted' if response.deleted_count > 0 else "document not found."}
