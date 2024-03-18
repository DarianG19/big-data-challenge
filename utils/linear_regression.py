from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd

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
