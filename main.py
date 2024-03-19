from readFiles import read_files
from diagrams import create_diagram
from mongoDB import get_data_from_mongodb


def main():
    read_files('./dataset/dataset')

    # Diagramme erstellen
    x_array, y_array = get_data_from_mongodb("dataWA")
    create_diagram(x_array, y_array)

    x_array, y_array = get_data_from_mongodb("data")
    create_diagram(x_array, y_array)


if __name__ == '__main__':
    main()
