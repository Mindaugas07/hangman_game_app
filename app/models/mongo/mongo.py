import datetime, os
from random import randint
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, List, Union
from pymongo.errors import ConfigurationError, PyMongoError


class MongoDB:
    try:

        def __init__(
            self, host: str, port: int, db_name: str, collection_name: str
        ) -> None:
            self.client = MongoClient(host, port)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]

    except ConfigurationError as e:
        print("Configuration error:", str(e))

    def find_documents(self, query: Dict, columns: Dict) -> List[Dict]:
        documents = self.collection.find(query, columns)
        return list(documents)

    def update_one_document(self, query: Dict, update: Dict) -> int:
        result = self.collection.update_one(query, {"$set": update})
        return result.modified_count

    def update_many_document(self, query: Dict, update: Dict) -> int:
        result = self.collection.update_many(query, {"$set": update})
        return result.modified_count

    def delete_one_documents(self, query: Dict) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many_documents(self, query: Dict) -> int:
        result = self.collection.delete_many(query)
        return result.deleted_count

    def insert_one_document(self, document: Dict) -> str:
        result = self.collection.insert_one(document)
        print(f"Printed result: {result}")
        return str(result.inserted_id)

    def insert_many_document(self, document: Dict) -> List[str]:
        result = self.collection.insert_many(document)
        # print(f"Printed result: {result}")
        return list(result.inserted_ids)

    # def generate_data_base(self, numb_of_documents):
    #     for _ in range(numb_of_documents):
    #         self.create_random_person()

    def query_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$eq": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_greater_than(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$gt": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_greater_than_or_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$gte": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_in_array(
        self, field_name: str, value: List, parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$in": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_less_than(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$lt": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_less_than_or_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$lte": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_not_equal(
        self, field_name: str, value: Union[str, int, float, bool], parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$ne": value}}
        result = self.collection.find(query, parameter)
        return list(result)

    def query_not_in_array(
        self, field_name: str, value: List, parameter: Dict = {}
    ) -> List[dict]:
        query = {field_name: {"$nin": value}}
        result = self.collection.find(query, parameter)
        return list(result)
