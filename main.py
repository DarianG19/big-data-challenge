from mongo_db import get_data
from utils.math_helpers import detrending


def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    data = list(get_data())
    for data_object in data:
        print(
            f"{data_object['file_name']}: {data_object['datasets'].keys()}")  # Um zu überprüfen, wie die Datasets
        # heißen, da diese noch nicht formatiert in der DB liegen

    x_file = "007ff213-9b5d-4243-9c8b-5eae997ac0ee.h5"
    y_file = "007ff213-9b5d-4243-9c8b-5eae997ac0ee.h5"

    x_axis_dataset = "timestamp"
    y_axis_dataset = "magnetization"

    # diagram_variant = "scatter" # "scatter

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
    # create_plot(x_axis_list, y_axis_list, x_axis_dataset, y_axis_dataset, diagram_variant)

    detrending(x_axis_list, y_axis_list)


if __name__ == '__main__':
    main()
