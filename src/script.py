import argparse
import os

import pymongo

import importer
MONGODB = pymongo.MongoClient(os.getenv('MONGODB'))


def main():
    MONGODB['importer'].command('ping')
    os.listdir(os.getenv('BASEPATH_DATA'))

    parser = argparse.ArgumentParser(description='Custom Importer')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
