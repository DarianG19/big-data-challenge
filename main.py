from mongo_db import get_data
from storing_files import read_and_store_locale_files


def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    data = list(get_data())
    for data_object in data:
        # Um zu überprüfen, wie die Datasets heißen, da diese noch nicht formatiert in der DB liegen
        print(f"{data_object['file_name']}: {data_object['datasets'].keys()}")

    # compare_datasets(data)

    # run_regression(x_axis_list, y_axis_list)
    # detrending(x_axis_list, y_axis_list)


if __name__ == '__main__':
    main()
