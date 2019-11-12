import os

import pymongo

import importer
import settings
from api import API
from preparation.base import WpPreparator


MONGODB = pymongo.MongoClient(os.getenv('MONGODB'))


def main():
    os.listdir(os.getenv('BASEPATH_DATA'))
    # db
    db = MONGODB[os.getenv('MONGODB_DATABASE')]
    db.command('ping')

    # api
    api = API(**settings.API)

    # parse
    WpPreparator.process('/../data/xml/wp_sample.xml', db)

    # import
    images = importer.ImageImporter(db, api)
    images.upload_all()

    sections = importer.SectionsImporter(db, api)
    sections.upload_all()


if __name__ == '__main__':
    main()
