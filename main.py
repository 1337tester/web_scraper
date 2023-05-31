from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values(dotenv_path=".env")

uri = f'mongodb+srv://m001-student:{config["PASS"]}@sandbox.wusok6y.mongodb.net/?retryWrites=true&w=majority'
print(uri)
# Create a new client and connect to the server
client = MongoClient(host=uri, server_api=ServerApi('1'))
db = client.get_database(name=config["DB_NAME"])
collection = db.get_collection(name=config["COL_NAME"])
# database = MongoClient[]
# Send a ping to confirm a successful connection
try:
    item = collection.find_one()
    print(type(item))
    print(20*"X")
    print(item)
    print(20*"X")
    print(f'Collection name - {db.list_collection_names()[0]}')
    print(20*"X")
    # print(f'Number of docs = {collection.count_documents(filter={})}')
    # result = collection.create_index([('URL', pymongo.ASCENDING)],unique=True)
    job = {"Jobs": "testinger", "URL": "wwssw.aaa.bbb"}
    result = collection.insert_one(document=job)
    print(f'Result is {result}')
    jobs = [{"Jobs": "testinger", "URL": "wwssw.aaa.bbb"},
            {"Jobs": "tetinger", "URL": "wws.aaa.bbb"},
            ]
    result_many = collection.insert_many(documents=jobs)
    collection.update_many(filter={},update={$set: {"Jobs": "testinger", "URL": "wwssw.aaa.bbb"}},upsert:True)
    print(f'Result_many is {result_many}')
except Exception as e:
    print(e)