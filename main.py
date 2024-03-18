from storing_files import read_and_store_locale_files
from mongo_db import get_data_for_specific_region_and_instrument


def main():
    # Lokale Dateien lesen und formatieren etc.
    read_and_store_locale_files('./dataset')

    # Mit korrigierten Daten aus DB arbeiten
    # data = get_data_for_specific_region_and_instrument('europe', 'unicorn')
    # for entry in data:
    #     print(entry)


if __name__ == '__main__':
    main()
