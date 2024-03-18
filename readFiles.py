import h5py
import os
from insertDataInMongoDB import insert_into_mongodb
from utils.format_strings import format_string
from utils.check_numeric import check_if_numeric


def list_files_in_path(path):
    # Listet alle Dateien im angegebenen Pfad auf
    return [os.path.join(path, file_name) for file_name in os.listdir(path) if
            os.path.isfile(os.path.join(path, file_name))]


def read_file(file_path, easter_egg_counter):
    try:
        with h5py.File(file_path, 'r') as f:
            # Überprüfen, ob 'data' oder 'Daten' vorhanden ist
            if 'data' in f:
                dataset_group = f['data']
            elif 'Daten' in f:
                dataset_group = f['Daten']
            else:
                return None, None, easter_egg_counter, (
                    f"Weder 'data' noch 'Daten' in der Datei '{os.path.basename(file_path)}'. "
                    f"Überspringe...")

            region_name = format_string(dataset_group.attrs.get("configuration", ""))
            instrument_name = format_string(dataset_group.attrs.get("instrument", ""))

            # Prüfe jedes Dataset in der Datagroup auf numerische Werte
            for dataset_name in dataset_group.keys():
                dataset = dataset_group[dataset_name]
                data = dataset[()]
                for index, entry in enumerate(data):
                    try:
                        check_if_numeric(entry)
                    except ValueError:
                        easter_egg_counter += 1
                        print(
                            f"Das Dataset '{dataset_name}' am Index {index} in '{os.path.basename(file_path)}' hat einen nicht-numerischen Wert '{entry}'.")
                        # TODO: Dateien entfernen aus dem gesamten Dataset

            return region_name, instrument_name, easter_egg_counter, None
    except Exception as e:
        return None, None, easter_egg_counter, f"Fehler beim Lesen der Datei! '{os.path.basename(file_path)}': {e}"


def update_counts(region_name, instrument_name, data_regions, data_instruments, regions_with_instruments):
    if region_name:
        # Regionen und Instrumente werden allgemein gezaehlt
        data_regions[region_name] = data_regions.get(region_name, 0) + 1
        data_instruments[instrument_name] = data_instruments.get(instrument_name, 0) + 1

        # Instrumente werden zu den entsprechenden Regionen gezaehlt
        if region_name not in regions_with_instruments:
            regions_with_instruments[region_name] = {}
        regions_with_instruments[region_name][instrument_name] = regions_with_instruments[region_name].get(
            instrument_name, 0) + 1


def print_summary(count_files, data_regions, data_instruments, regions_with_instruments, easter_egg_counter):
    print(f"Anzahl der Dateien, die durchlaufen werden: {count_files}")
    print(f"Regionen: {data_regions}")
    print(f"Instrumente: {data_instruments}", end="\n\n")

    for region, instruments in regions_with_instruments.items():
        sum_of_instruments_per_region = sum(instruments.values())
        print(f"{region.upper()}")
        for instrument, count in instruments.items():
            print(f"{instrument}: {count}")
        print(f"SUM: {sum_of_instruments_per_region}")
        print("---------------")

    print(f"Easter Egg Counter: {easter_egg_counter}")


def read_files(path):
    easter_egg_counter = 0
    count_files = 0
    data_regions = {}
    data_instruments = {}
    regions_with_instruments = {}

    file_paths = list_files_in_path(path)
    for file_path in file_paths:
        count_files += 1
        region_name, instrument_name, easter_egg_counter, error_message = read_file(file_path, easter_egg_counter)
        if error_message:
            print(error_message)
            continue

        update_counts(region_name, instrument_name, data_regions, data_instruments, regions_with_instruments)

    print_summary(count_files, data_regions, data_instruments, regions_with_instruments, easter_egg_counter)
