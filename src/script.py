import argparse
import os

import pymongo
MONGODB = pymongo.MongoClient(os.getenv('MONGODB'))


def main():
    MONGODB['importer'].command('ping')

    parser = argparse.ArgumentParser(description='Custom Importer')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
