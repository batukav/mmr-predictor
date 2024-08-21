import pymongo
from database import database
from pymongo import MongoClient
from typing import Dict, Any, TypedDict

# to-do :  _DocumentType typehint ??

JsonObject = Dict[str, Any]

def print_generic_exception(method_name:str, exception:str)->str :
    message = f"Some error occurred in {method_name}:{exception}"
    return message

class MongoDB(database):
    
    def __init__(self, host = 'localhost', port = 27017, user = None, password = None):
        
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        
    def connect_db(self):
        
        method_name = self.my_method.__name__
        try:
            client = MongoClient(self.host, self.password)
        except Exception as e:
            raise RuntimeWarning(print_generic_exception(method_name, e))
        
        self.client = client
        
        return client
    
    def get_database(self, database_name = None):
        
        method_name = self.my_method.__name__
        try:
            db = self.client[databasename]
            self.db = db
        except Exception as e:
            raise RuntimeWarning(print_generic_exception(method_name, e))

        return db
    
    def get_collection(self, collection_name:str = None) -> TypedDict:
        
        try:
            collection = self.db[collection_name]
        except Exception as e:
            raise RuntimeWarning(print_generic_exception(method_name, e))
        
        return collection
    
    def insert_item(self, collection_name:str, item:JsonObject) -> any:
        
        collection = get_collection(collection_name)
        
        try:
            insert_id = collection.insert_one(item).inserted_id
        except Exception as e:
            raise RuntimeWarning(print_generic_exception(method_name, e))
        
        return insert_id
        
    def get_item(self, query:any):
        
        collection = get_collection(collection_name)
        
        try:
            item = collection.find_one(query)
        except Exception as e:
            raise RuntimeWarning(print_generic_exception(method_name, e))
        
        return item
        
        
        
        
        
        
        
        