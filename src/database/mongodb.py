import pymongo
from database import database
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, Any, TypedDict, List, Union

JsonObject = Dict[str, Any]


class MongoDB(database):

    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        username: str = None,
        password: str = None,
    ):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect_db(self) -> MongoClient:

        try:
            client = MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
        except Exception as e:
            raise RuntimeError(f"Some error occurred in connect_db: {e}")

        self.client = client

        return client

    def get_database(self, database_name: str = None) -> Database:

        try:
            db = self.client[database_name]
            self.db = db
        except Exception as e:
            raise RuntimeError(f"Some error occurred in get_database: {e}")

        return db

    def get_collection(self, collection_name: str = None) -> Collection:

        try:
            collection = self.db[collection_name]
        except Exception as e:
            raise RuntimeError(f"Some error occurred in get_collection: {e}")

        self.collection_name = collection_name

        return collection

    def insert_item(self, collection_name: str, item: Union[Dict, List[Dict]]) -> any:

        collection = self.get_collection(collection_name)

        if isinstance(item, list):

            try:
                collection.insert_many(item)
            except Exception as e:
                raise RuntimeError(
                    f"Some error occurred while adding multiple items at once: {e}"
                )

        else:
            try:
                insert_id = collection.insert_one(item).inserted_id
            except Exception as e:
                raise RuntimeError(f"Some error occurred in insert_item: {e}")

            return insert_id

    def get_item(self, query: any = None):

        collection = self.get_collection(self.collection_name)

        try:
            item = collection.find_one(query)
        except Exception as e:
            raise RuntimeError(f"Some error occurred in get_item: {e}")

        return item

    def get_all_items(self) -> pymongo.cursor.Cursor:

        collection = self.get_collection(self.collection_name)

        try:
            all_items = collection.find()
        except Exception as e:
            raise RuntimeError(f"Some error occurred in get_all_items: {e}")

        self.all_items = all_items
        return all_items
