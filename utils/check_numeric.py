def check_if_numeric(wert):
    # Überprüfen, ob der Wert numerisch ist
    if isinstance(wert, (int, float)):
        return True
    else:
        # Versuchen, den Wert in Float umzuwandeln, falls es sich um eine numerische Zeichenkette handelt
        try:
            float(wert)
            return True
        except ValueError:
            # Eine Fehlermeldung ausgeben, wenn der Wert nicht numerisch ist
            raise ValueError(f"Fehler: '{wert}' ist kein numerischer Wert.")


# Beispiele zur Verwendung der Funktion
try:
    check_if_numeric(142.752)  # Sollte keinen Fehler ausgeben
except ValueError as e:
    print(e)

try:
    check_if_numeric("easteregg :)")  # Sollte eine Fehlermeldung ausgeben
except ValueError as e:
    print(e)
