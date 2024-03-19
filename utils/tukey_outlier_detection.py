from scipy.stats import iqr
import numpy as np
from utils.check_numeric import check_and_edit_not_numeric


def delete_outliers(data_object):
    # Durchführung der Tukey-Ausreißererkennung für jedes Dataset
    for dataset_name, dataset_values in data_object['datasets'].items():

        # Konvertiere alle Werte in numerische Werte
        for i, value in enumerate(dataset_values):
            # Überprüfe, ob der Index i gültig ist
            if i < len(dataset_values):
                dataset_values[i] = check_and_edit_not_numeric(value)

        q1 = np.percentile(dataset_values, 25)
        q3 = np.percentile(dataset_values, 75)
        iqr_value = iqr(dataset_values)
        lower_bound = q1 - 1.5 * iqr_value
        upper_bound = q3 + 1.5 * iqr_value

        # Ausreißer identifizieren
        outliers = [i for i, value in enumerate(dataset_values) if value < lower_bound or value > upper_bound]

        # Prozentsatz der Ausreißer berechnen
        outlier_percentage = (len(outliers) / len(dataset_values)) * 100

        # Ausgabe in der Konsole
        # print(f"Ausreißer im Datensatz '{dataset_name}':")
        # print(f"Anzahl der Ausreißer: {len(outliers)}")
        # print(f"Prozentualer Anteil der Ausreißer: {outlier_percentage:.2f}%")

        # Ausreißer aus dem aktuellen Dataset entfernen und auch aus anderen Datensätzen entfernen
        for outlier_index in sorted(outliers, reverse=True):
            for other_dataset_name, other_dataset_values in data_object['datasets'].items():
                if dataset_name != other_dataset_name and outlier_index < len(other_dataset_values):
                    del other_dataset_values[outlier_index]

        # Bereinigten Datensatz speichern
        cleaned_dataset = [value for i, value in enumerate(dataset_values) if i not in outliers]
        data_object['datasets'][dataset_name] = cleaned_dataset

    return data_object
