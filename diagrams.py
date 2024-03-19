import matplotlib.pyplot as plt
import pandas as pd


def create_diagram(x_array, y_array):
    """
    Funktion zum Erstellen von Graphen (aktuell Plots)
    :param x_array: Datenset für die Abszisse
    :param y_array: Datenset für Ordinate
    """
    plt.plot(x_array, y_array)

    plt.title('Diagramm')
    plt.xlabel('Distance')
    plt.ylabel('Magnetization')

    plt.show()


def plot_regions_with_instruments(regions_with_instruments):
    # Sammeln Sie die Daten für das Balkendiagramm
    labels = []
    counts = []

    for region, instruments_count in regions_with_instruments.items():
        for instrument, count in instruments_count.items():
            labels.append(f"{region} - {instrument}")
            counts.append(count)

    # Organisieren Sie die Daten für das Balkendiagramm
    data = {'Labels': labels, 'Count': counts}
    df = pd.DataFrame(data)

    # Erstellen Sie das Balkendiagramm
    plt.figure(figsize=(12, 8))
    bars = plt.barh(df['Labels'], df['Count'])

    # Fügen Sie die Beschriftungen zu den Balken hinzu
    for bar, label in zip(bars, labels):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, label, va='center')

    # Fügen Sie Achsenbeschriftungen und Titel hinzu
    plt.xlabel('Anzahl')
    plt.ylabel('Region - Instrument')
    plt.title('Kombinationen von Region und Instrument')

    # Zeigen Sie das Balkendiagramm an
    plt.show()
