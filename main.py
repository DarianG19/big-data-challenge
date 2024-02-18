from readFiles import read_files
from readFiles import createDiagram

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


if __name__ == '__main__':
     read_files('./dataset/dataset')

     #createDiagram(graph_data[0], graph_data[1])
