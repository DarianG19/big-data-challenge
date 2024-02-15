import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

from utils.format_strings import format_dataset


def read_files(path):
    """
    Funktion zum Einlesen der Dateien in einem bestimmten Pfad.
    :param path: Der Pfad zum jeweiligen Ordner
    :return:
    """

    # Iterate through files in folder
    for file_name in os.listdir(path):
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

                # group_x = np.arange(1, 1001)
                dataset_list = []
                for dataset in dataset_group:
                    formatted_dataset = format_dataset(dataset)

                    dataset_list.append(formatted_dataset)
                    # group_y = np.array(dataset_group[dataset])

                print(dataset_list)
            except Exception as e:  # TODO: Aktuell werden jegliche Fehler abgefangen, muss spezifischer werden,
                # um "fehlerhafte" Dateien/Daten dennoch auszulesen
                print(f"Fehler beim Lesen der Datei! '{file_name}': {e}")
                continue
        else:
            print(f"{file_path} skipped ... ")


def createDiagram(x_array, y_array):
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
