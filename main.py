from readFiles import read_files
from readFiles import createDiagram
from pymongo import MongoClient

mongo_uri = "mongodb+srv://<noahkuse>:<BigDMitBigD>@bigdataproject.f6aka7m.mongodb.net/"
client = MongoClient(mongo_uri)
db = client.bigdataproject  # Ändere 'mydatabase' entsprechend deiner Datenbank

try:
    # Einfache Abfrage, um sicherzustellen, dass die Verbindung funktioniert
    result = db.mycollection.find_one()
    print("Verbindung erfolgreich. Beispiel-Dokument:", result)
except Exception as e:
    print(f"Fehler bei der Datenbankabfrage: {e}")


#if __name__ == '__main__':
     #read_files('./dataset/dataset')

     #createDiagram(graph_data[0], graph_data[1])
