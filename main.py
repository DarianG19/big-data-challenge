import numpy as np
from matplotlib import pyplot as plt

from mongo_db import get_data, insert_into_mongodb
from utils.math_helpers import detrending


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


def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    all_x = []
    all_y = []
    data = list(get_data())
    for data_object in data:
        # Um zu überprüfen, wie die Datasets heißen, da diese noch nicht formatiert in der DB liegen
        print(f"{data_object['file_name']}: {data_object['datasets'].keys()}")

        all_x.extend(data_object["datasets"]["magnetization"])
        all_y.extend(data_object["datasets"]["wall_thickness"])

    create_heatmap(all_x, all_y)

    # compare_datasets(data)

    # run_regression(x_axis_list, y_axis_list)
    # detrending(x_axis_list, y_axis_list)


def detrend_magnetizations_with_timestamps(data_obj):
    try:
        detrended_magnetization = detrending(data_obj["datasets"]["timestamp"], data_obj["datasets"]["magnetization"])
        data_obj["datasets"]["magnetization"] = detrended_magnetization
    except Exception as e:
        print(e)
    finally:
        return data_obj


if __name__ == '__main__':
    main()
