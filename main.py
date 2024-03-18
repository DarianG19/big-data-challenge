from storing_files import read_and_store_locale_files
from mongo_db import get_data_for_specific_region_and_instrument


def main():
    # Lokale Dateien lesen und formatieren etc.
    # read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    data = list(get_data_for_specific_region_and_instrument('asia', 'dolphin'))
    for data_object in data:
        print(f"{data_object['file_name']}: {data_object['datasets'].keys()}") # Um zu überprüfen, wie die Datasets heißen, da diese noch nicht formatiert in der DB liegen


if __name__ == '__main__':
    main()
