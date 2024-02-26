from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def insert_into_mongodb(data_list):
    # Create a new client and connect to the server
    uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['BigDataProject']
    collection = database['DatasetBigD']

    try:
        collection.insert_many(data_list)
        print(f'{len(data_list)} Daten erfolgreich in MongoDB eingefügt')
    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()
