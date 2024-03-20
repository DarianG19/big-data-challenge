import csv

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from mongo_db import get_data, insert_into_mongodb
from storing_files import read_and_store_locale_files
from utils.check_numeric import check_and_edit_not_numeric
from utils.math_helpers import detrending, detrending_with_regression, detrending_sklearn, polynom_regression
from diagrams import plot_dataset_with_timestamps

def create_heatmap(all_x, all_y):
    # Filtere NaN-Werte aus den Daten
    mask = ~np.isnan(all_x) & ~np.isnan(all_y)  # Erstellt eine Maske für Werte, die in beiden Arrays nicht NaN sind
    filtered_x = np.array(all_x)[mask]  # Anwenden der Maske auf all_x
    filtered_y = np.array(all_y)[mask]  # Anwenden der Maske auf all_y

    # Erstellung des 2D-Histogramms mit den gefilterten Daten
    heatmap, xedges, yedges = np.histogram2d(filtered_x, filtered_y, bins=(500, 500))
    extent = [np.min(filtered_x), np.max(filtered_x), np.min(filtered_y), np.max(filtered_y)]

    # Heatmap zeichnen
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', aspect="auto")
    plt.colorbar()
    plt.show()


def create_heatmap_seaborn(all_x, all_y):
    # Filtere NaN-Werte aus den Daten
    # mask = ~np.isnan(all_x) & ~np.isnan(all_y)
    # filtered_x = np.array(all_x)[mask]
    # filtered_y = np.array(all_y)[mask]

    # Erstellung des 2D-Histogramms mit den gefilterten Daten
    # heatmap, xedges, yedges = np.histogram2d(filtered_x, filtered_y, bins=(500, 500))
    #
    # # Seaborn Heatmap erstellen
    # plt.clf()
    # sns.heatmap(heatmap, cmap='hot', cbar=True)
    plot = sns.jointplot(x=all_x, y=all_y, kind='hex', gridsize=30, cmap='plasma', marginal_kws=dict(bins=50))
    plot.set_axis_labels("Wandstärke", "Magnetisierung")
    plt.tight_layout()
    plt.show()


def main():
    # read_and_store_locale_files("./dataset")
    all_x = []
    all_y = []
    all_y_other = []
    data = list(get_data())
    for data_object in data:
        print(f"{data_object['file_name']}: {data_object['datasets'].keys()}")

        # Minimale Länge bestimmen, um sicherzustellen, dass beide Arrays gleich lang sind
        min_length = min(len(data_object["datasets"]["timestamp"]), len(data_object["datasets"]["magnetization"]),
                         len(data_object["datasets"]["wall_thickness"]))

        # Arrays auf minimale Länge kürzen
        timestamps = np.array(data_object["datasets"]["timestamp"][:min_length])
        magnetizations = np.array(data_object["datasets"]["magnetization"][:min_length])
        wall_thicknesses = np.array(data_object["datasets"]["wall_thickness"][:min_length])

        # Detrending durchführen
        detrended_magnetizations_with_regression = detrending_with_regression(timestamps, magnetizations)
        detrended_magnetization = detrending_sklearn(timestamps, magnetizations)

        # Detrendete Magnetisierungsdaten und Wandstärkendaten hinzufügen
        all_x.extend(wall_thicknesses)
        all_y.extend(detrended_magnetizations_with_regression)
        # all_y_other.extend(detrended_magnetization)

    create_heatmap_seaborn(all_x, all_y)
    polynom_regression(all_x, all_y)
    # create_heatmap_seaborn(all_x, all_y_other)

    # compare_datasets(data)

    # run_regression(x_axis_list, y_axis_list)
    # detrending(x_axis_list, y_axis_list)


def detrend_magnetizations_with_timestamps(data_obj):
    detrended_magnetization = []
    try:
        detrended_magnetization = detrending(data_obj["datasets"]["magnetization"])
        # data_obj["datasets"]["magnetization"] = detrended_magnetization
    except Exception as e:
        print(e)
    finally:
        return detrended_magnetization


def konvertieren():
    data = list(get_data())

    with open("datenwerte.csv", "w", newline="") as w_file:
        wwriter = csv.writer(w_file)
        wwriter.writerow(["Typ", "Wert"])

        for obj in data:
            for dataset_name, values in obj["datasets"].items():
                for index, value in enumerate(values):
                    try:
                        wert = check_and_edit_not_numeric(value)
                        # print(f"Typ: {type(wert)}, Value: {wert}")
                        wwriter.writerow([type(wert).__name__, wert])
                    except ValueError:
                        with open('daten_typen.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            fehlermeldung = f"Fehler: '{obj["file_name"]}'; Index {index} -> 'Typ: {type(value)}, Value: {value}'."
                            writer.writerow([fehlermeldung])


if __name__ == '__main__':
    main()
    # konvertieren()
