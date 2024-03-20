import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime


# Die restlichen Importe und Hilfsfunktionen bleiben unverändert

def plot_dataset_with_timestamps(timestamps, values, dataset_name):
    # Konvertiere Timestamps von Bytes zu Strings und dann zu datetime-Objekten, falls notwendig
    timestamps = [datetime.strptime(ts.decode('utf-8'), "%Y-%m-%dT%H:%M:%S") if isinstance(ts, bytes) else ts for ts in
                  timestamps]

    # Erstelle das Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(timestamps, values, marker='.', linestyle='-')
    plt.title(f'{dataset_name} over Time')
    plt.xlabel('Timestamp')
    plt.ylabel(dataset_name.capitalize())

    # Formatierung der X-Achse als Datum
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%dT%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()  # Rotation

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


def create_regression_scatter_plot(x_test, y_test, y_pred):
    plt.scatter(x_test, y_test, color='red', label='Tatsächliche Werte')
    plt.plot(x_test, y_pred, color='blue', linewidth=2, label='Vorhersagen')
    plt.xlabel('Timestamp')
    plt.ylabel('Velocity')
    plt.title('Lineare Regression - Velocity vs. Timestamps')
    plt.legend()
    plt.show()


def create_plot(x_axis_values, y_axis_values, x_axis_name, y_axis_name, variant):
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.title(f"Verhaeltnis - {y_axis_name} vs. {x_axis_name}")

    if variant == "scatter":
        plt.scatter(x_axis_values, y_axis_values, marker='.', linestyle='-', color='blue', label="Werte")
    elif variant == "line":
        plt.plot(x_axis_values, y_axis_values, color='blue', linewidth=1, label='Werte')

    plt.legend()
    plt.show()


def compare_datasets(data):
    x_file = "fc616e10-4b61-46e5-9205-52722424aa35.h5"
    y_file = "fc616e10-4b61-46e5-9205-52722424aa35.h5"
    x_axis_dataset = "timestamp"
    y_axis_dataset = "velocity"
    diagram_variant = "scatter" # "scatter" oder "line"
    x_axis_list = []
    y_axis_list = []
    for dataset_object in data:
        if dataset_object["file_name"] == x_file:
            x_axis_list = dataset_object["datasets"][x_axis_dataset]  # Werte aus dem gewünschten Dataset extrahieren
        if dataset_object["file_name"] == y_file:
            y_axis_list = dataset_object["datasets"][y_axis_dataset]  # Werte aus dem gewünschten Dataset extrahieren
    # Anpassung der Längen der Listen, nachdem beide initialisiert wurden
    if len(x_axis_list) > len(y_axis_list):
        x_axis_list = x_axis_list[:len(y_axis_list)]
    else:
        y_axis_list = y_axis_list[:len(x_axis_list)]

    create_plot(x_axis_list, y_axis_list, x_axis_dataset, y_axis_dataset, diagram_variant)



