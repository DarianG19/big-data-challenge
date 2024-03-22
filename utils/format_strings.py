import re


def format_string(dataset_name: str) -> str:
    dataset_name = dataset_name.lower()
    without_spaces = re.sub(r'\s+', "", dataset_name)  # Leerzeichen entfernen
    return re.sub(r'^_+|_+$', "", without_spaces)  # Unterstriche am Anfang und Ende # entfernen


def sort_data(list_x, list_y):
    """
    List x = timestamps = [[72452342.324, 7343553.893457], [6234234.92412, 6383945.12364]]
    List y = magnetizations = [[-2.2342, 1.12341], [-5.87234, -2.2342]]
    :param list_x: Timestamps
    :param list_y: Magnetizations
    """

    # Paare von Elementen aus list_x und list_y bilden und gemeinsam sortieren
    gepaarte_und_sortierte_listen = sorted(zip(list_x, list_y), key=lambda paar: paar[0][0])

    # Die sortierten Paare wieder in separate Listen trennen
    sortierte_list_x, sortierte_list_y = zip(*gepaarte_und_sortierte_listen)

    # Da zip Tuples zurückgibt, konvertieren wir sie zurück in Listen
    sortierte_list_x = [element for sublist in sortierte_list_x for element in sublist]
    sortierte_list_y = [element for sublist in sortierte_list_y for element in sublist]

    return sortierte_list_x, sortierte_list_y
