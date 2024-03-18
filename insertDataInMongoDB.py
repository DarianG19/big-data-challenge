from pymongo.mongo_client import MongoClient


def insert_into_mongodb(data_dict):
    # Erstelle einen neuen Client und verbinde dich mit dem Server
    uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    database = client['BigDataProject']
    collection = database['data']

    try:
        # Füge die Daten in MongoDB ein
        collection.insert_one(data_dict)
        print(f'Daten erfolgreich in MongoDB eingefügt')

    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()
