import re


def format_dataset(dataset_name: str) -> str:
    dataset_name = dataset_name.lower()
    without_spaces = re.sub(r'\s+', "", dataset_name)  # Leerzeichen entfernen
    return re.sub(r'^_+|_+$', "", without_spaces)  # Unterstriche am Anfang und Ende # entfernen
