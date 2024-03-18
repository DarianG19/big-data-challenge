from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
database = client['BigDataProject']


def insert_into_mongodb(data_dict):
    # Erstelle einen neuen Client und verbinde dich mit dem Server
    collection = database['data2']

    try:
        # Füge die Daten in MongoDB ein
        collection.insert_one(data_dict)
        print(f'Daten erfolgreich in MongoDB eingefügt')

    except Exception as e:
        print(f'Fehler beim Einfügen in MongoDB: {e}')
    finally:
        client.close()


def get_data_from_mongodb():
    collection = database['dataWithoutAusreißer']

    query = {'region': 'europe', 'instrument': 'unicorn'}

    try:
        return collection.find(query)
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []

