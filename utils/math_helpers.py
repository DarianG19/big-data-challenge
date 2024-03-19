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

    # Plot der Originaldaten und der detrendeten Daten
    # plt.figure(figsize=(12, 6))
    # plt.subplot(1, 2, 1)
    # plt.scatter(x_list, y_list, label='Originaldaten')
    # plt.title('Originaldaten mit Trend')
    # plt.xlabel('Zeit')
    # plt.ylabel('Wert')
    # plt.legend()
    #
    # # Smoothing aktuell doch nicht nötig
    # # smoothed_y = savgol_filter(detrended_y_list, window_length=51, polyorder=3)
    #
    # # Vergleich der Originaldaten, detrendeten und geglätteten Daten
    # plt.figure(figsize=(12, 6))
    # plt.scatter(x_list, y_list, label='Originaldaten')
    # plt.scatter(x_list, detrended_y_list, label='Detrendete Daten')
    # # plt.scatter(x_list, smoothed_y, label='Geglättete Daten', color='red')
    # plt.legend()
    # plt.show()

    return detrended_y_list


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
