from pymongo.mongo_client import MongoClient


def insert_into_mongodb(data_dict):
    if data_dict.get('instrument') == "pufferfish" and data_dict.get('region') == "australia":
        # Erstelle einen neuen Client und verbinde dich mit dem Server
        uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(uri)
        database = client['BigDataProject']
        collection = database['dataWA']

        try:
            # Füge die Daten in MongoDB ein
            collection.insert_one(data_dict)
            print(f'Daten erfolgreich in MongoDB eingefügt')

        except Exception as e:
            print(f'Fehler beim Einfügen in MongoDB: {e}')
        finally:
            client.close()


def get_data_from_mongodb(collection_name):
    """
    Funktion zum Abrufen von Daten aus MongoDB
    :param collection_name: Name der MongoDB-Sammlung
    :return: Arrays für x- und y-Achsen
    """
    # Verbindung zur MongoDB herstellen
    uri = "mongodb+srv://noahkuse:BigDMitBigD@bigdataproject.f6aka7m.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    database = client['BigDataProject']
    collection = database[collection_name]

    # Arrays für die x- und y-Achsen initialisieren
    x_array = []
    y_array = []

    # Daten aus der MongoDB abrufen und Arrays füllen
    for data_object in collection.find({"instrument": "pufferfish", "region": "australia"}):
        # print("Data object:", data_object)  # Debugging-Anweisung
        if "datasets" in data_object:
            datasets = data_object["datasets"]
            for dataset in datasets:
                # print("Dataset:", dataset)  # Debugging-Anweisung
                x_array.append(dataset["distance"])
                y_array.append(dataset["magnetization"])

    # Verbindung zur MongoDB schließen
    client.close()

    return x_array, y_array
