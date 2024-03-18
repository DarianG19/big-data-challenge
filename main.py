from diagrams import create_scatter_plot
from storing_files import read_and_store_locale_files
from mongo_db import get_data_for_specific_region_and_instrument


def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    data = list(get_data_for_specific_region_and_instrument('asia', 'dolphin'))
    for data_object in data:
        print(
            f"{data_object['file_name']}: {data_object['datasets'].keys()}")  # Um zu überprüfen, wie die Datasets heißen, da diese noch nicht formatiert in der DB liegen

    x_file = "012dd33a-c1a7-4e9d-91cb-7de11e82f976.h5"
    y_file = "012dd33a-c1a7-4e9d-91cb-7de11e82f976.h5"

    x_axis_dataset = "timestamp"
    y_axis_dataset = "defect_channel"

    x_axis_list = []
    y_axis_list = []

    for dataset_object in data:
        if dataset_object["file_name"] == x_file:
            x_axis_list = dataset_object["datasets"][x_axis_dataset]  # Werte aus dem gewünschten Dataset extrahieren
        if dataset_object["file_name"] == y_file:
            y_axis_list = dataset_object["datasets"][y_axis_dataset]  # Werte aus dem gewünschten Dataset extrahieren

    # Anpassung der Längen der Listen, nachdem beide initialisiert wurden
    if len(x_axis_list) > len(y_axis_list):
        x_axis_list = x_axis_list[:len(y_axis_list)]
    else:
        y_axis_list = y_axis_list[:len(x_axis_list)]

    print(len(x_axis_list), len(y_axis_list))
    create_scatter_plot(x_axis_list, y_axis_list, x_axis_dataset, y_axis_dataset)


if __name__ == '__main__':
    main()
