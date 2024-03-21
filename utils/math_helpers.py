import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy.polynomial.polynomial import Polynomial
from scipy import signal
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from diagrams import create_regression_scatter_plot


def run_regression(x_list, y_list):
    df = pd.DataFrame({
        'Timestamps': x_list,
        'Magnetization': y_list,
    })

    # Daten für das Training und Testen vorbereiten
    x = df['Timestamps'].values.reshape(-1, 1)  # Feature Matrix
    y = df['Magnetization'].values  # Target Vector

    # Datensatz in Trainings- und Testset aufteilen
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # Lineares Regressionsmodell erstellen und trainieren
    model = LinearRegression()
    model.fit(x_train, y_train)

    # Vorhersagen treffen
    y_pred = model.predict(x_test)
    create_regression_scatter_plot(x_test, y_test, y_pred)

    return y_pred.tolist()


def detrending(y_list):
    detrended_y_list = signal.detrend(y_list)

    return detrended_y_list


def detrend_magnetizations_with_timestamps(data_obj):
    detrended_magnetization = []
    try:
        detrended_magnetization = detrending(data_obj["datasets"]["magnetization"])
        # data_obj["datasets"]["magnetization"] = detrended_magnetization
    except Exception as e:
        print(e)
    finally:
        return detrended_magnetization


def detrending_with_regression(time_array, data_array):
    coefficients = np.polyfit(time_array, data_array, 1)  # '1' steht für den Grad des Polynoms, linear in diesem Fall
    trend = np.polyval(coefficients, time_array)

    # Detrendete Daten berechnen, indem der Trend von den Originaldaten abgezogen wird
    detrended_data = data_array - trend

    # plt.figure(figsize=(10, 5))
    # plt.scatter(time_array, data_array, label='Originaldaten')
    # plt.plot(time_array, trend, label='Trend', linestyle='--')
    # plt.scatter(time_array, detrended_data, label='Detrendete Daten', marker='o')
    # plt.legend()
    # plt.show()
    return detrended_data


def detrending_sklearn(x_values, y_values):
    try:
        model = LinearRegression()
        model.fit(x_values.reshape(-1, 1), y_values)

        residuale = y_values - model.predict(x_values.reshape(-1, 1)) + np.mean(y_values[:20])
        return list(residuale)
    except Exception as e:
        print(f"Error: {e}")  # TODO: manchmal kommt noch "Error: Input y contains NaN


def detrending_polynomial(x_list, y_list):
    # Polynomisches Modell anpassen
    p = Polynomial.fit(x_list, y_list, deg=2)

    # Polynomischen Trend entfernen
    detrended_y = y_list - p(x_list)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(x_list, y_list, label='Originaldaten')
    plt.title('Mit nichtlinearem Trend')
    plt.subplot(1, 2, 2)
    plt.scatter(x_list, detrended_y, label='Detrendete Daten', color='orange')
    plt.title('Nach polynomischem Detrending')
    plt.tight_layout()
    plt.show()


def polynom_regression(x, y):
    coefficients = np.polyfit(x, y, 3)

    # Erzeugen Sie ein Polynomobjekt aus den Koeffizienten, um das Polynom einfacher auswerten zu können
    polynom = np.poly1d(coefficients)

    # Generieren Sie Werte für x, um die Vorhersagen des Modells zu plotten
    x_lin = np.linspace(min(x), max(x), 500)  # 500 Punkte zwischen dem minimalen und maximalen Wert von x

    # Nutzen Sie das Polynomobjekt, um Vorhersagen basierend auf x_lin zu machen
    y_pred = polynom(x_lin)

    # Plotten der Originaldaten und der Polynomregressionskurve
    plt.plot(x_lin, y_pred, color='green', label='Polynomregression 3. Grades')  # Regressionskurve
    plt.title('Polynomregression 3. Grades')
    plt.xlabel('Wandstaerke')
    plt.ylabel('Magnetisierung')
    plt.legend()
    plt.show()
