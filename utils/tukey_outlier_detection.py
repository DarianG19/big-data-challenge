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
            for dataset_name, dataset in f.items():
                # Convert dataset to numpy array
                # data = np.array(dataset, dtype=float)

                # Print content of dataset
                print(f"Content of Dataset '{dataset_name}':")
                print(data)

                # Tukey outlier detection
                outliers = tukey_outlier_detection(data)

                # Remove outliers from data
                cleaned_data = [x for x in data if x not in outliers]

                # Calculate percentage of outliers
                percentage_outliers = len(outliers) / len(data) * 100

                print(f"Dataset: {dataset_name}")
                print(f"Total outliers: {len(outliers)}")
                print(f"Percentage outliers: {percentage_outliers:.2f}%")
                print("------------")

    except Exception as e:
        print(f"Fehler beim Lesen der Datei! '{file_path}': {e}")