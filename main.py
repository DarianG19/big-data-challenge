import numpy as np

from diagrams import create_heatmap_seaborn, create_plot, plot_dataset_with_timestamps
from mongo_db import get_data
from utils.format_strings import format_timestamps
from utils.math_helpers import detrending_sklearn, calculateMeanMinMax


def main():
    # read_and_store_locale_files("./dataset")
    all_x = []
    all_y = []
    all_timestamps = []
    all_magnetization = []
    all_detrended_magnetization = []
    all_velocity = []
    all_wallthickness = []

    data = list(get_data())
    for data_object in data:
        # print(f"{data_object['file_name']}: {data_object['datasets'].keys()}")

        # Minimale Länge bestimmen, um sicherzustellen, dass Arrays gleich lang sind
        min_length = min(len(data_object["datasets"]["timestamp"]), len(data_object["datasets"]["magnetization"]),
                         len(data_object["datasets"]["wall_thickness"]), len(data_object["datasets"]["defect_channel"]),
                         len(data_object["datasets"]["velocity"]))

        # Alle Werte in Listen schreiben
        # all_timestamps.extend(data_object["datasets"]["timestamp"])
        # all_velocity.extend(data_object["datasets"]["velocity"])
        # all_magnetization.extend(data_object["datasets"]["magnetization"])
        all_wallthickness.extend(data_object["datasets"]["wall_thickness"])

        # Arrays auf minimale Länge kürzen
        timestamps = np.array(data_object["datasets"]["timestamp"][:min_length])
        defect_channels = np.array(data_object["datasets"]["defect_channel"][:min_length])
        magnetizations = np.array(data_object["datasets"]["magnetization"][:min_length])
        wall_thicknesses = np.array(data_object["datasets"]["wall_thickness"][:min_length])
        velocity = np.array(data_object["datasets"]["velocity"][:min_length])

        # Detrending durchführen
        detrended_magnetization = detrending_sklearn(timestamps, magnetizations)

        # Detrendete Magnetisierungsdaten und Wandstärkendaten hinzufügen

        all_detrended_magnetization.extend(detrended_magnetization)
        # all_x.extend(detrended_magnetization)
        # all_y.extend(detrended_magnetization)

    fehlerhafte_timestamps, formatted_timestamps = format_timestamps(all_timestamps)
    # create_plot(formatted_timestamps, all_y, "Timestamp", "Magnetisierung", "scatter")
    # create_plot(formatted_timestamps, all_velocity, "Timestamp", "Velocity", "scatter")
    # plot_dataset_with_timestamps(formatted_timestamps, magnetization, "Magnetisierung")
    # print(fehlerhafte_timestamps)
    # create_heatmap_seaborn(all_x, all_y)

    print("Mean                     Min                          Max")
    print(calculateMeanMinMax(all_wallthickness))


if __name__ == '__main__':
    main()
