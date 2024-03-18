import os

import h5py


def list_files_in_path(path):
    """Listet alle Dateien im angegebenen Pfad auf."""
    return [os.path.join(path, file_name) for file_name in os.listdir(path) if
            os.path.isfile(os.path.join(path, file_name))]


def extract_datasets(file_path):
    """Extrahiert Datasets aus einer h5-Datei und gibt eine Datengruppe zurück."""
    with h5py.File(file_path, 'r') as f:
        if 'data' in f:
            return f['data']
        elif 'Daten' in f:
            return f['Daten']
    return None

