class StoredAttachmentsManager:
    PROVIDER_ID_FIELD = 'id'
    URL_FIELD = 'url'
    CAPTION_FIELD = 'content'
    CREDIT_FIELD = 'excerpt'

    items_collection = 'attachments'
    response_collection = 'imported_images'
    original_key_fields = ['id', 'url']
        # item = {i: original_item[i] for i in self.original_key_fields}

    # def __init__(self, roar_id, attachments_source):
    def __init__(self, db):
        self.db = db

    def get_image_info_by_id(self, attachment_id):
        item = self.db[self.response_collection].find_one({'id': attachment_id})
        if item:
            return item['response']
        raise KeyError()

    def get_image_info_by_url(self, url):
        item = self.db[self.response_collection].find_one({'url': url})
        if item:
            return item['response']
        raise KeyError()

    def get_caption_and_credit(self, attachment_id):
        # return (caption, credit)
        item = self.db[self.items_collection].find_one({'id': attachment_id})
        return (item['content'] or '', item['excerpt'] or '')
