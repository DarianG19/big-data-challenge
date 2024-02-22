import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

from utils.format_strings import format_string


def read_files(path):
    count_files = 0
    data_regions = {}
    data_instruments = {}
    regions_with_instruments = {}

    # Iterate through files in folder
    for file_name in os.listdir(path):
        count_files += 1
        file_path = os.path.join(path, file_name)

        # Check, if file_path is a file and not a folder
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

                # Regionen und Instrumente werden allgemein gezaehlt
                if region_name in data_regions:
                    data_regions[region_name] += 1
                else:
                    data_regions[region_name] = 1

                if instrument_name in data_instruments:
                    data_instruments[instrument_name] += 1
                else:
                    data_instruments[instrument_name] = 1

                # Instrumente werden zu den entsprechenden Regionen gezaehlt
                if region_name not in regions_with_instruments:
                    regions_with_instruments[region_name] = {instrument_name: 1}
                elif instrument_name not in regions_with_instruments[region_name]:
                    regions_with_instruments[region_name][instrument_name] = 1
                else:
                    regions_with_instruments[region_name][instrument_name] += 1

                # group_x = np.arange(1, 1001)
                dataset_list = []
                for dataset in dataset_group:
                    formatted_dataset = format_string(dataset)
                    dataset_list.append(formatted_dataset)

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
