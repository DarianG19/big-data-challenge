import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_and_visualize_data(visualization_data_x, visualization_data_y):
    visualization_data_x = np.array(visualization_data_x)
    visualization_data_y = np.array(visualization_data_y)

    indices = np.argsort(visualization_data_x)

    visualization_data_x = visualization_data_x[indices]
    visualization_data_y = visualization_data_y[indices]

    indices_to_delete = np.where(visualization_data_x < 0)
    visualization_data_x = np.delete(visualization_data_x, indices_to_delete)
    visualization_data_y = np.delete(visualization_data_y, indices_to_delete)

    indices_to_delete = np.where(visualization_data_x > 35)
    visualization_data_x = np.delete(visualization_data_x, indices_to_delete)
    visualization_data_y = np.delete(visualization_data_y, indices_to_delete)

    # Die Funktion, die an die Daten angepasst werden soll

    def modell_funktion_polynom_3(x, a, b, c, d):
        return a * x ** 3 + b * x ** 2 + c * x + d

    def modell_funktion_sinus(x, a, b, c, d):
        return a * np.sin(b * x + c) + d

    def modell_funktion_cosinus(x, a, b, c, d):
        return a * np.cos(b * x + c) + d

    # curve_fit benutzen, um die Parameter a und b zu finden
    parameter, parameter_kovarianz = curve_fit(modell_funktion_polynom_3, visualization_data_x, visualization_data_y)

    y_vorhersage = modell_funktion_polynom_3(visualization_data_x, *parameter)

    ss_res = np.sum((visualization_data_y - y_vorhersage) ** 2)
    ss_tot = np.sum((visualization_data_y - np.mean(visualization_data_y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    print(f"R^2: {r2}")

    print("Gefundene Parameter:", parameter)

    # Die gefundene Kurve zeichnen
    plot = sns.jointplot(x=visualization_data_x, y=visualization_data_y, kind='hex', gridsize=100, cmap="Blues",
                         marginal_kws=dict(bins=50))
    plt.plot(visualization_data_x, modell_funktion_polynom_3(visualization_data_x, *parameter), label='Polynom 3. Grades',
             color='red')
    plot.set_axis_labels("Wandstärke", "Magnetisierung")
    plt.legend()
    plt.tight_layout()
    plt.show()

