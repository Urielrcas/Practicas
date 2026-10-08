import os
import random
from dotenv import load_dotenv
from pymongo import MongoClient
import dns.resolver


load_dotenv()

mongo_user = os.getenv("Mongo_User")
mongo_pass = os.getenv("Mongo_Password")
mongo_cluster = os.getenv("Mongo_Cluster")
mongo_db_name = os.getenv("Mongo_db")
mongo_collection = os.getenv("Mongo_Colleccion")

if not all([mongo_user, mongo_pass, mongo_cluster, mongo_db_name, mongo_collection]):
    raise ValueError("Faltan variables en el archivo .env")

mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_cluster}/?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
coleccion = db[mongo_collection]

productos = ["Laptop", "Tablet", "Celular", "Monitor"]

ventas = []
for _ in range(2):
    venta = {
        "producto": random.choice(productos),
        "cantidad": random.randint(1, 5)
    }
    ventas.append(venta)

coleccion.insert_many(ventas)
print("Datos generados correctamente.")