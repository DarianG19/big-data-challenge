from scipy.stats import iqr


def process_datasets(data_object):
    for dataset_name, dataset_values in data_object['datasets'].items():
        # Durchführung der Tukey-Ausreißererkennung
        q1 = np.percentile(dataset_values, 25)
        q3 = np.percentile(dataset_values, 75)
        iqr_value = iqr(dataset_values)
        lower_bound = q1 - 1.5 * iqr_value
        upper_bound = q3 + 1.5 * iqr_value

        # Ausreißer identifizieren
        outliers = [value for value in dataset_values if value < lower_bound or value > upper_bound]

        # Prozentsatz der Ausreißer berechnen
        outlier_percentage = (len(outliers) / len(dataset_values)) * 100

        # Ausgabe in der Konsole
        print(f"Ausreißer im Datensatz '{dataset_name}':")
        print(f"Anzahl der Ausreißer: {len(outliers)}")
        print(f"Prozentualer Anteil der Ausreißer: {outlier_percentage:.2f}%")

        # Ausreißer aus dem Datensatz entfernen
        cleaned_dataset = [value for value in dataset_values if value >= lower_bound and value <= upper_bound]
        data_object['datasets'][dataset_name] = cleaned_dataset

    return data_object
