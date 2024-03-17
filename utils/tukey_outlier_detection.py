import h5py
import numpy as np


def tukey_outlier_detection(data, multiplier=1.5):
    data = np.array(data, dtype=float)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    cleaned_data = [x for x in data if x not in outliers]
    return cleaned_data


def process_datasets(file_path):
    cleaned_datasets = {}  # Dictionary to store cleaned datasets
    total_outliers = 0  # Total number of outliers in all datasets
    try:
        with h5py.File(file_path, 'r') as f:
            for dataset_name, dataset in f.items():
                # Convert dataset to numpy array
                data = np.array(dataset)

                # Tukey outlier detection
                cleaned_data, outliers = tukey_outlier_detection(data)

                # Store cleaned data
                cleaned_datasets[dataset_name] = cleaned_data

                # Calculate percentage of outliers
                percentage_outliers = len(outliers) / len(data) * 100
                total_outliers += len(outliers)

                print(f"Dataset: {dataset_name}")
                print(f"Total outliers: {len(outliers)}")
                print(f"Percentage outliers: {percentage_outliers:.2f}%")
                print("------------")

    except Exception as e:
        print(f"Fehler beim Lesen der Datei! '{file_path}': {e}")

    return cleaned_datasets
