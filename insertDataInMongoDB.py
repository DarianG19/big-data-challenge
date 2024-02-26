from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def insert_into_mongodb(region, instrument, count):
    uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client['BigDataProject']
    collection = database['DatasetBigD']

    data = {
        'region': region,
        'instrument': instrument,
        'count': count
    }

    try:
        collection.insert_one(data)
        print(f'Daten erfolgreich in MongoDB eingefügt: {data}')
    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()