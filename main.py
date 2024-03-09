from readFiles import read_files
from readFiles import read_and_insert_h5_file


def main():
    read_files('./dataset')
    read_and_insert_h5_file("./dataset/dataset/0a7e8940-9008-45fa-9a99-054757404083.h5")


if __name__ == '__main__':
    main()
