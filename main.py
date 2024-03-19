#from diagrams import create_plot
#from storing_files import read_and_store_locale_files
#from mongo_db import get_data_for_specific_region_and_instrument


#def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
#   data = list(get_data_for_specific_region_and_instrument('asia', 'dolphin'))
#   for data_object in data:
#        print(
#            f"{data_object['file_name']}: {data_object['datasets'].keys()}")  # Um zu überprüfen, wie die Datasets heißen, da diese noch nicht formatiert in der DB liegen
#
 ##   x_file = "012dd33a-c1a7-4e9d-91cb-7de11e82f976.h5"
 #   y_file = "012dd33a-c1a7-4e9d-91cb-7de11e82f976.h5"

#    x_axis_dataset = "timestamp"
#    y_axis_dataset = "velocity"

#    diagram_variant = "line"

#    x_axis_list = []
#    y_axis_list = []
#
##    for dataset_object in data:
#        if dataset_object["file_name"] == x_file:
#            x_axis_list = dataset_object["datasets"][x_axis_dataset]  # Werte aus dem gewünschten Dataset extrahieren
#        if dataset_object["file_name"] == y_file:
#            y_axis_list = dataset_object["datasets"][y_axis_dataset]  # Werte aus dem gewünschten Dataset extrahieren
#
    # Anpassung der Längen der Listen, nachdem beide initialisiert wurden
#    if len(x_axis_list) > len(y_axis_list):
#        x_axis_list = x_axis_list[:len(y_axis_list)]
#    else:
#        y_axis_list = y_axis_list[:len(x_axis_list)]

#    print(len(x_axis_list), len(y_axis_list))
#    create_plot(x_axis_list, y_axis_list, x_axis_dataset, y_axis_dataset, diagram_variant)
#
#
#if __name__ == '__main__':
#    main()

from diagrams import create_plot
from storing_files import read_and_store_locale_files
from mongo_db import get_data_for_specific_region_and_instrument
import numpy as np
import hdbscan
import matplotlib.pyplot as plt


#from mongo_db import get_data_for_specific_region_and_instrument
def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus der DB arbeiten
    data = list(get_data_for_specific_region_and_instrument('asia', 'dolphin'))
    print("Geladene Daten aus der Datenbank:", data)  # Debugging-Ausgabe

    # Stellen Sie sicher, dass die Daten geladen wurden
    if not data:
        print("Keine Daten aus der Datenbank geladen.")
        return

    # Überprüfung der Datenstruktur
    for data_object in data:
        print(f"{data_object['file_name']} hat folgende Datasets: {list(data_object['datasets'].keys())}")

    x_file = "012dd33a-c1a7-4e9d-91cb-7de11e82f976.h5"
    y_file = "012dd33a-c1a7-4e9d-91cb-7de11e82f976.h5"

    x_axis_dataset = "timestamp"
    y_axis_dataset = "magnetization"

    # Initialisieren der Listen
    x_axis_list = []
    y_axis_list = []

    # Daten aus der geladenen Daten extrahieren
    for dataset_object in data:
        if dataset_object["file_name"] == x_file:
            x_axis_list = dataset_object["datasets"].get(x_axis_dataset, [])
        if dataset_object["file_name"] == y_file:
            y_axis_list = dataset_object["datasets"].get(y_axis_dataset, [])

    print(f"x_axis_list (nach Extraktion): {x_axis_list}")  # Debugging-Ausgabe
    print(f"y_axis_list (nach Extraktion): {y_axis_list}")  # Debugging-Ausgabe

    # Prüfen, ob die Listen Daten enthalten
    if len(x_axis_list) > 0 and len(y_axis_list) > 0:
        if len(x_axis_list) > len(y_axis_list):
            x_axis_list = x_axis_list[:len(y_axis_list)]
        else:
            y_axis_list = y_axis_list[:len(x_axis_list)]

        # Clustering mit HDBSCAN
        combined_data = np.array(list(zip(x_axis_list, y_axis_list))).reshape(-1, 2)
        clusterer = hdbscan.HDBSCAN(min_cluster_size=5)  # Anpassen des min_cluster_size je nach Bedarf
        labels = clusterer.fit_predict(combined_data)

        # Visualisierung des Clustering-Ergebnisses
        plt.figure(figsize=(10, 6))  # Größenanpassung für eine bessere Darstellung
        unique_labels = set(labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = 'k'  # Schwarz für Rauschen
            class_member_mask = (labels == k)
            xy = combined_data[class_member_mask]
            plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)
        plt.title("HDBSCAN Clustering")
        plt.xlabel(x_axis_dataset)
        plt.ylabel(y_axis_dataset)
        plt.show()
    else:
        print("Eine oder beide der Datenlisten sind leer. Kein Clustering möglich.")

    # Erstellen des ursprünglichen Plots, falls benötigt
    create_plot(x_axis_list, y_axis_list, x_axis_dataset, y_axis_dataset, "line")

if __name__ == '__main__':
    main()
