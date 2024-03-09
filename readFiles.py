import h5py
import matplotlib.pyplot as plt
import os
from insertDataInMongoDB import insert_regioninstrument_into_mongodb
from insertDataInMongoDB import insert_h5file_into_mongodb
from utils.format_strings import format_string


def read_files(path):
    count_files = 0
    data_regions = {}
    data_instruments = {}
    regions_with_instruments = {}
    data_list = []

    # Iterate durch Dateien im Ordner
    for file_name in os.listdir(path):
        count_files += 1
        file_path = os.path.join(path, file_name)

        # Überprüfen, ob file_path eine Datei und kein Ordner ist
        if os.path.isfile(file_path):
            try:
                f = h5py.File(f'{file_path}', 'r')
                list(f.keys())

                # Überprüfen, ob 'data' oder 'Daten' vorhanden ist
                if 'data' in f:
                    dataset_group = f['data']
                elif 'Daten' in f:
                    dataset_group = f['Daten']
                else:
                    print(f"Weder 'data' noch 'Daten' in der Datei '{file_name}'. Überspringe...")
                    continue

                region_name = format_string(dataset_group.attrs.get("configuration"))
                instrument_name = format_string(dataset_group.attrs.get("instrument"))

                # Regionen und Instrumente werden allgemein gezählt
                if region_name in data_regions:
                    data_regions[region_name] += 1
                else:
                    data_regions[region_name] = 1

                if instrument_name in data_instruments:
                    data_instruments[instrument_name] += 1
                else:
                    data_instruments[instrument_name] = 1

                # Instrumente werden zu den entsprechenden Regionen gezählt
                if region_name not in regions_with_instruments:
                    regions_with_instruments[region_name] = {instrument_name: 1}
                elif instrument_name not in regions_with_instruments[region_name]:
                    regions_with_instruments[region_name][instrument_name] = 1
                else:
                    regions_with_instruments[region_name][instrument_name] += 1

                # Füge die Daten zur Batch-Liste hinzu
                data_list.append({
                    'region': region_name,
                    'instrument': instrument_name,
                    'count': regions_with_instruments[region_name][instrument_name]
                })

            except Exception as e:
                print(f"Fehler beim Lesen der Datei! '{file_name}': {e}")
                continue
        else:
            print(f"{file_path} skipped ... ")

        # Überprüfe, ob genügend Daten für einen Batch vorhanden sind (z.B., 100 Dokumente pro Batch)
        if len(data_list) >= 100:
            # Rufe die Funktion auf, um die Daten in MongoDB als Batch einzufügen

            # (auskommentiert, müssen ja nicht immer die Daten einfügen)
            # insert_regioninstrument_into_mongodb

            # Leere die Liste für den nächsten Batch
            data_list = []

    # Am Ende der Schleife füge die verbleibenden Daten ein
    if data_list:
        insert_regioninstrument_into_mongodb(data_list)

    print(f"Anzahl der Dateien, die durchlaufen werden: {count_files}")
    print(f"Regionen: {data_regions}")
    print(f"Instrumente: {data_instruments}", end="\n\n")

    for region in regions_with_instruments:
        sum_of_instruments_per_region = sum(regions_with_instruments[region].values())
        print(f"{region.upper()}")
        for instrument, count in regions_with_instruments[region].items():
            print(f"{instrument}: {count}")
        print(f"SUM: {sum_of_instruments_per_region}")
        print("---------------")


def read_and_insert_h5_file(file_path):
    """
    Diese Funktion liest eine einzelne h5-Datei ein und schreibt den Inhalt in eine MongoDB-Datenbank.
    :param file_path: Der Pfad zur h5-Datei.
    """
    try:
        with h5py.File(file_path, 'r') as f:
            data_dict = {'file_path': file_path}

            for group_name, group in f.items():
                for dataset_name, dataset in group.items():
                    # Wandele Numpy-Array in Python-Liste um
                    data_array = dataset[:]
                    data_dict[dataset_name] = data_array.tolist()

            if len(data_dict) > 1:  # Überprüfe, ob mindestens ein Datensatz gefunden wurde
                insert_h5file_into_mongodb(data_dict)
                print(f'Daten aus Datei {file_path} erfolgreich in MongoDB eingefügt')

    except Exception as e:
        print(f"Fehler beim Lesen der Datei! '{file_path}': {e}")


def create_diagram(x_array, y_array):
    """
    Funktion zum Erstellen von Graphen (aktuell Plots)
    :param x_array: Datenset für die Abszisse
    :param y_array: Datenset für Ordinate
    """
    plt.plot(x_array, y_array)

    plt.title('Diagramm')
    plt.xlabel('')
    plt.ylabel('Distance')

    plt.show()
