import os

import pymongo

import importer
MONGODB = pymongo.MongoClient(os.getenv('MONGODB'))


def main():
    MONGODB[os.getenv('MONGODB_DATABASE')].command('ping')
    os.listdir(os.getenv('BASEPATH_DATA'))


if __name__ == '__main__':
    main()
