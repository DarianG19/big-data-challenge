from pymongo.mongo_client import MongoClient

from utils.format_strings import format_string

uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
database = client['BigDataProject']


def insert_into_mongodb(data_dict):
    if data_dict.get('instrument') == "dog" and data_dict.get('region') == "europe":
        # Erstelle einen neuen Client und verbinde dich mit dem Server
        collection = database['dataEuropeDog']

        try:
            # Füge die Daten in MongoDB ein
            collection.insert_one(data_dict)
            print(f'Daten erfolgreich in MongoDB eingefügt')

        except Exception as e:
            print(f'Fehler beim Einfügen in MongoDB: {e}')
        finally:
            client.close()


def get_data():
    collection = database['dataWA']
    try:
        return collection.find()
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []


def get_data_for_specific_region_and_instrument(region, instrument):
    collection = database['dataWithoutAusreißer']

    query = {'region': format_string(region), 'instrument': format_string(instrument)}

    try:
        return collection.find(query)
    except Exception as e:
        print(f"Fehler beim Abrufen der Daten: {e}")
        return []
