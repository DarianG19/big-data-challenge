import re

import numpy as np


def format_string(dataset_name: str) -> str:
    dataset_name = dataset_name.lower()
    without_spaces = re.sub(r'\s+', "", dataset_name)  # Leerzeichen entfernen
    return re.sub(r'^_+|_+$', "", without_spaces)  # Unterstriche am Anfang und Ende # entfernen


def format_timestamps(array):
    neues_array = []  # Eine temporäre Liste, um die aktualisierten Werte zu speichern
    fehlerhafte_timestamps = []

    for timestamp in array:
        # Versucht, den Wert in eine Fließkommazahl zu konvertieren, wenn es sich nicht bereits um eine solche handelt
        if not isinstance(timestamp, float):
            try:
                timestamp = float(timestamp)
            except ValueError:
                fehlerhafte_timestamps.append(timestamp)
                continue  # Geht zum nächsten Timestamp über, wenn die Konvertierung fehlschlägt

        # Wenn der Wert negativ ist, entfernen Sie das Minus
        if timestamp < 0:
            timestamp = abs(timestamp)

        neues_array.append(timestamp)  # Fügt den angepassten Wert dem neuen Array hinzu

    return np.array(fehlerhafte_timestamps), np.array(neues_array)
