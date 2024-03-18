import re


def check_if_numeric(wert):
    # Behandelt numerische Werte direkt
    if isinstance(wert, (int, float)):
        return True

    # Dekodiert Bytes zu Strings
    if isinstance(wert, bytes):
        wert = wert.decode('utf-8')

    # Ab hier ist 'wert' entweder ein String oder war ursprünglich ein String
    try:
        # Versucht, den Wert in eine Fließkommazahl zu konvertieren
        float(wert)
        return True
    except ValueError:
        # Überprüft, ob der Wert einem Timestamp-Format entspricht
        timestamp_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?.*$'

        if re.match(timestamp_pattern, wert):
            return True
        else:
            # Gibt eine Fehlermeldung aus, wenn der Wert weder numerisch noch ein Timestamp ist
            raise ValueError(f"Fehler: '{wert}' ist weder ein numerischer Wert noch ein gültiger Timestamp.")
