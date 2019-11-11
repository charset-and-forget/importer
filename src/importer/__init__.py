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
            try:
                self.upload(original_item)
            except Exception as e:
                failed.append((original_item, e))
        return failed

    def upload(self, original_item):
        raise NotImplementedError

    def _iter_source_items(self):
        raise NotImplementedError

    def _is_processed(self, original_item):
        raise NotImplementedError

    def _store_response(self, original_item, response):
        # store response and item's key in destination collection for future
        raise NotImplementedError


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
