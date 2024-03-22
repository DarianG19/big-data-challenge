import hdbscan
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def applyhdbscan(data, min_cluster_size=5):
    """
    Anwenden des HDBSCAN-Clustering-Algorithmus auf die Daten.
    :param data: Die Daten für das Clustering (numpy array von Form (n_samples, n_features)).
    :param min_cluster_size: Die minimale Größe eines Clusters.
    :return: clusterer, labels, probabilities
    """
    # Initialisieren und Trainieren des HDBSCAN-Clusteralgorithmus
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, gen_min_span_tree=True)
    clusterer.fit(data)

    # Extrahiere die Cluster-Zuweisungen und Wahrscheinlichkeiten
    labels = clusterer.labels
    probabilities = clusterer.probabilities_

    # Optional: Rückgabe des Clusteralgorithmus selbst, um weitere Analysen durchzuführen
    return clusterer, labels, probabilities


def clustering(x_list, y_list):
    x = np.array(x_list)
    y = np.array(y_list)

    # Kombinieren der Arrays in ein 2D-NumPy-Array
    data = np.vstack([x, y]).T

    # Erstellen des HDBSCAN-Clustering-Objekts
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2, gen_min_span_tree=True)

    # Durchführung des Clusterings
    clusterer.fit(data)

    # Ergebnisse
    print("Cluster-Labels:", clusterer.labels_)

    # Visualisierung
    # plt.scatter(x, y, c=clusterer.labels_, cmap='plasma', marker='o')
    # plt.title('HDBSCAN Clustering')
    # plt.xlabel('Wall_Thickness')
    # plt.ylabel('Magnetization')
    # plt.colorbar(label='Cluster Label')
    # plt.show()

    plot = sns.jointplot(x=x, y=y, kind='hex', gridsize=30, cmap='plasma', marginal_kws=dict(bins=50))
    plot.set_axis_labels("Wandstärke", "Magnetisierung")
    plt.tight_layout()
    plt.show()
