import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


# Die restlichen Importe und Hilfsfunktionen bleiben unverändert

def plot_dataset(timestamps, values, dataset_name, file_name):
    # Konvertiere Timestamps von Bytes zu Strings und dann zu datetime-Objekten, falls notwendig
    timestamps = [datetime.strptime(ts.decode('utf-8'), "%Y-%m-%dT%H:%M:%S") if isinstance(ts, bytes) else ts for ts in
                  timestamps]

    # Erstelle das Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(timestamps, values, marker='.', linestyle='-')
    plt.title(f'{dataset_name} over Time in {file_name}')
    plt.xlabel('Timestamp')
    plt.ylabel(dataset_name.capitalize())

    # Formatierung der X-Achse als Datum
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%dT%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()  # Rotation

    plt.show()


def create_scatter_plot(x_test, y_test, y_pred):
    plt.scatter(x_test, y_test, color='red', label='Tatsächliche Werte')
    plt.plot(x_test, y_pred, color='blue', linewidth=2, label='Vorhersagen')
    plt.xlabel('Timestamp')
    plt.ylabel('magnetization')
    plt.title('Lineare Regression - Magnetisierung vs. Timestamps')
    plt.legend()
    plt.show()
