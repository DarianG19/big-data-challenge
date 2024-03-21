import numpy as np

from diagrams import create_heatmap_seaborn
from mongo_db import get_data
from utils.math_helpers import detrending_sklearn
from utils.curve_fit import analyze_and_visualize_data


def main():
    # read_and_store_locale_files("./dataset")
    all_x = []
    all_y = []
    data = list(get_data())
    for data_object in data:
        print(f"{data_object['file_name']}: {data_object['datasets'].keys()}")

        # Minimale Länge bestimmen, um sicherzustellen, dass Arrays gleich lang sind
        min_length = min(len(data_object["datasets"]["timestamp"]), len(data_object["datasets"]["magnetization"]),
                         len(data_object["datasets"]["wall_thickness"]))

        # Arrays auf minimale Länge kürzen
        timestamps = np.array(data_object["datasets"]["timestamp"][:min_length])
        magnetizations = np.array(data_object["datasets"]["magnetization"][:min_length])
        wall_thicknesses = np.array(data_object["datasets"]["wall_thickness"][:min_length])

        # Detrending durchführen
        detrended_magnetization = detrending_sklearn(timestamps, magnetizations)

        # Detrendete Magnetisierungsdaten und Wandstärkendaten hinzufügen
        all_x.extend(wall_thicknesses)
        all_y.extend(detrended_magnetization)

    analyze_and_visualize_data(all_x, all_y)

    # create_heatmap_seaborn(all_x, all_y)


if __name__ == '__main__':
    main()
