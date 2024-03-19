from mongo_db import get_data, insert_into_mongodb
from utils.math_helpers import detrending


def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    data = list(get_data())
    for data_object in data:
        # Um zu überprüfen, wie die Datasets heißen, da diese noch nicht formatiert in der DB liegen
        print(f"{data_object['file_name']}: {data_object['datasets'].keys()}")
        new_data_obj = detrend_magnetizations_with_timestamps(data_object)
        insert_into_mongodb(new_data_obj, "data_wa_demg")

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
