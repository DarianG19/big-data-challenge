import h5py
import matplotlib.pyplot as plt
import os
from insertDataInMongoDB import insert_into_mongodb
from utils.format_strings import format_string
from utils.tukey_outlier_detection import process_datasets


def read_files(path):
    count_files = 0
    data_regions = {}
    data_instruments = {}
    regions_with_instruments = {}

    # Iterate durch Dateien im Ordner
    for file_name in os.listdir(path):
        count_files += 1
        file_path = os.path.join(path, file_name)

        # Überprüfen, ob file_path eine Datei und kein Ordner ist
        if os.path.isfile(file_path):
            try:
                with h5py.File(file_path, 'r') as f:
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
                    data_regions.setdefault(region_name, 0)
                    data_regions[region_name] += 1

                    data_instruments.setdefault(instrument_name, 0)
                    data_instruments[instrument_name] += 1

                    # Instrumente werden zu den entsprechenden Regionen gezählt
                    regions_with_instruments.setdefault(region_name, {})
                    regions_with_instruments[region_name].setdefault(instrument_name, 0)
                    regions_with_instruments[region_name][instrument_name] += 1

                    # Erstelle ein Objekt für jede h5-Datei
                    data_object = {
                        'file_name': file_name,
                        'region': region_name,
                        'instrument': instrument_name,
                        'count': regions_with_instruments[region_name][instrument_name],
                        'datasets': {}
                    }

                    # Füge jedes Dataset-Array zum Objekt hinzu
                    for dataset_name in dataset_group.keys():
                        # Wandele Numpy-Array in Python-Liste um
                        data_array = dataset_group[dataset_name][:]
                        data_object['datasets'][dataset_name] = data_array.tolist()

                    # Process datasets for outliers
                    process_datasets(data_object)

                    # Füge das Objekt zur MongoDB hinzu
                    # insert_into_mongodb(data_object)
                    # print(f'Daten aus Datei {file_path} erfolgreich in MongoDB eingefügt')

            except Exception as e:
                print(f"Fehler beim Lesen der Datei! '{file_name}': {e}")
                continue
        else:
            print(f"{file_path} skipped ... ")

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
