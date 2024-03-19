import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from mongo_db import get_data, insert_into_mongodb
from utils.math_helpers import detrending, detrending_with_regression


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
    mask = ~np.isnan(all_x) & ~np.isnan(all_y)
    filtered_x = np.array(all_x)[mask]
    filtered_y = np.array(all_y)[mask]

    # Erstellung des 2D-Histogramms mit den gefilterten Daten
    heatmap, xedges, yedges = np.histogram2d(filtered_x, filtered_y, bins=(500, 500))

    # Seaborn Heatmap erstellen
    plt.clf()
    sns.heatmap(heatmap, cmap='hot', cbar=True)
    plt.show()


def main():
    all_x = []
    all_y = []
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
        detrended_magnetizations = detrending_with_regression(timestamps, magnetizations)

        # Detrendete Magnetisierungsdaten und Wandstärkendaten hinzufügen
        all_x.extend(detrended_magnetizations)
        all_y.extend(wall_thicknesses)

    create_heatmap_seaborn(all_x, all_y)

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


if __name__ == '__main__':
    main()
