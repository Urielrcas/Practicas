import os
from pathlib import path
from dotenv import load_dotenv

load_dotenv()


mongo_user = os.getenv("Mongo_User")
mongo_pass = os.getenv("Mongo_Password")
mongo_cluster = os.getenv("Mongo_Cluster")
mongo_db_name = os.getenv("Mongo_db")
mongo_collection = os.getenv("Mongo_Colleccion")

mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_cluster}"

