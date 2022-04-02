from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv('CONNECTION_STRING')

client = MongoClient(connection_string)
db = client['FLIGHT-SAVE']