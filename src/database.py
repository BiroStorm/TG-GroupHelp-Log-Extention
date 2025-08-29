import os
from pymongo import MongoClient
from dotenv import load_dotenv
import logging
import sys

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('MONGO_DB_NAME')

class Database:
    _client = None
    _db = None

    @classmethod
    def get_db(self):
        
        if self._db is None:
            try:
                self._client = MongoClient(MONGO_URI)
                self._db = self._client[DB_NAME]
                print("Connected to MongoDB.")
                logging.info("Connected to MongoDB.")
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                logging.error(f"Error connecting to MongoDB: {e}")
                sys.exit(1)
                self._db = None
                
        return self._db

    @classmethod
    def close_connection(self):
        if self._client:
            self._client.close()
            print("MongoDB connection closed.")
            logging.info("MongoDB connection closed.")

db = Database.get_db()
