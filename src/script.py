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
    WpPreparator.process('/data/wp_sample.xml', db)

    # import
    images = importer.ImageImporter(db, api)
    failed_images = images.upload_all()
    print(len(failed_images))

    authors = importer.AuthorsImporter(db, api)
    failed_authors = authors.upload_all()
    print(len(failed_authors))

    sections = importer.SectionsImporter(db, api)
    failed_sections = sections.upload_all()
    print(len(failed_sections))

    posts = importer.PostsImporter(db, api)
    failed_posts = posts.upload_all()
    print(len(failed_posts))


if __name__ == '__main__':
    main()
