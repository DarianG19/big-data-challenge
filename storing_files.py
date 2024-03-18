import os
from mongo_db import insert_into_mongodb
from reading_files import extract_datasets, list_files_in_path
from utils.format_strings import format_string
from utils.check_numeric import check_if_numeric


def validate_and_prepare_dataset(dataset_group, dataset_name, easter_egg_counter):
    """Validiert die Daten in einem Dataset und bereitet sie für die weitere Verarbeitung vor."""
    dataset = dataset_group[dataset_name]
    data = dataset[:]
    valid_data = []

    for index, entry in enumerate(data):
        if check_if_numeric(entry):
            valid_data.append(entry)
        else:
            easter_egg_counter += 1
            print(f"Das Dataset '{dataset_name}' am Index {index} hat einen nicht-numerischen Wert '{entry}'.")

    return valid_data, easter_egg_counter


def prepare_data_object(file_path, dataset_group, region_name, instrument_name, easter_egg_counter):
    """Bereitet ein Datenobjekt für MongoDB vor und validiert die Daten."""
    data_object = {
        'file_name': os.path.basename(file_path),
        'region': region_name,
        'instrument': instrument_name,
        'datasets': {}
    }

    for dataset_name in dataset_group:
        valid_data, easter_egg_counter = validate_and_prepare_dataset(dataset_group, dataset_name,
                                                                      easter_egg_counter)
        data_object['datasets'][dataset_name] = valid_data

    return data_object, easter_egg_counter


def process_and_store_data(file_path, easter_egg_counter):
    """Verarbeitet eine Datei und speichert die Daten in MongoDB."""
    dataset_group = extract_datasets(file_path)
    if not dataset_group:
        return None, None, easter_egg_counter, "Keine relevante Datengruppe gefunden."

    region_name = format_string(dataset_group.attrs.get("configuration", ""))
    instrument_name = format_string(dataset_group.attrs.get("instrument", ""))

    data_object, easter_egg_counter = prepare_data_object(file_path, dataset_group, region_name, instrument_name, easter_egg_counter)

    insert_into_mongodb(data_object)

    return region_name, instrument_name, easter_egg_counter, None


def read_and_store_locale_files(path):
    """Liest, formatiert und speichert lokale Dateien in der Cloud."""
    easter_egg_counter = 0
    file_paths = list_files_in_path(path)
    for file_path in file_paths:
        region_name, instrument_name, easter_egg_counter, error_message = process_and_store_data(file_path,
                                                                                                 easter_egg_counter)
        if error_message:
            print(error_message)
            continue
