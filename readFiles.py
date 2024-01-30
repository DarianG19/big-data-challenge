import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


def read_files(path):
    """
    Funktion zum Einlesen der Dateien in einem bestimmten Pfad.
    TODO: Aktuell wird ein Pfad zu einer Datei angegeben.
    :param path: Der Pfad zum jeweiligen Ordner
    :return:
    """
    f = h5py.File('{}'.format(path), 'r')
    list(f.keys())
    dsetGroup = f['data']
    group_x = np.arange(1, 1001)
    dset_list = []
    for dset in dsetGroup:
        dset_list.append(dset)
        group_y = np.array(dsetGroup[dset])

        createDiagram(group_x, group_y)
    print(dset_list)


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