class ItemUploader:
    source_collection = None
    destination_collection = None
    original_key_fields = []

    def __init__(self, db, api):
        self.db = db
        self.api = api

    def upload_all(self):
        failed = []
        for original_item in self._iter_source_items():
            if self._is_processed(original_item):
                continue
            try:
                self.upload(original_item)
            except Exception as e:
                failed.append((original_item, e))
        return failed

    def upload(self, original_item):
        raise NotImplementedError

    def _iter_source_items(self):
        collection = self.db[self.source_collection]
        for item in collection.find({}):
            yield item

    def _is_processed(self, original_item):
        collection = self.db[self.destination_collection]
        query = {i: original_item[i] for i in self.original_key_fields}
        return bool(collection.find(query))

    def _store_response(self, original_item, response):
        # store response and item's key in destination collection for future
        collection = self.db[self.destination_collection]
        item = {i: original_item[i] for i in self.original_key_fields}
        item['response'] = response
        return collection.insert_one(item)


class ImageUploader(ItemUploader):
    source_collection = 'attachments'
    destination_collection = 'uploaded_images'
    original_key_fields = ['id', 'url']

    def upload(self, original_item):
        response = self.api.upload_image(
            image_url=original_item['url'],
            caption=original_item['content'],
            credit=original_item['excerpt'],
            # alt='',
        )
        self._store_response(original_item, response)
