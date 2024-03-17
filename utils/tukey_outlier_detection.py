import h5py
import numpy as np


def tukey_outlier_detection(data, multiplier=1.5):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    return outliers


def process_datasets(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            print(f"Inhalt der Datei '{file_path}':")
            for dataset_name, dataset in f.items():
                print(f"Dataset '{dataset_name}':")
                print(dataset[()])  # Correct way to access dataset content

    except Exception as e:
        print(f"Fehler beim Lesen der Datei! '{file_path}': {e}")