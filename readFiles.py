import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


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
                f = h5py.File('{}'.format(file_path), 'r')
                list(f.keys())

                # Überprüfen, ob 'data' oder 'Daten' vorhanden ist
                if 'data' in f:
                    dsetGroup = f['data']
                elif 'Daten' in f:
                    dsetGroup = f['Daten']
                else:
                    print("Weder 'data' noch 'Daten' in der Datei '{}'. Überspringe...".format(file_name))
                    continue

                # group_x = np.arange(1, 1001)
                dset_list = []
                for dset in dsetGroup:
                    dset_list.append(dset)
                    # group_y = np.array(dsetGroup[dset])

                #print(dset_list)
            except Exception as e: # TODO: Aktuell werden jegliche Fehler abgefangen, muss spezifischer werden, um "fehlerhafte" Dateien/Daten dennoch auszulesen
                print("Fehler beim Lesen der Datei '{}': {}".format(file_name, str(e)))
                continue
        else:
            print("{} skipped ... ".format(file_path))


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