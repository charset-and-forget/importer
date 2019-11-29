import collections
import datetime
import re

# from scraper.embed_facade import get_embed


class FieldHandlers:
    @classmethod
    def as_is(cls, value):
        return value

    @classmethod
    def wp_pub_date(cls, value):
        dt = datetime.datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %z')
        return int(dt.timestamp())

    @classmethod
    def basename(cls, value):
        filtered_value = re.sub(r'[^\w\d_-]', cls._sub_empty, value)
        return filtered_value[:200]

    @staticmethod
    def _sub_empty(value):
        return ''


class PostBuilder(object):
    primitive_mapping = {
        # 'post_field': (wp_field, parse_func),
        'headline': ('title', FieldHandlers.as_is),
        'body': ('content', FieldHandlers.as_is),
        'subheadline': ('excerpt', FieldHandlers.as_is),
        'manual_basename': ('name', FieldHandlers.basename),
    }

    # meta
    IMAGE_POSTMETA_KEYS = ['_thumbnail_id']
    EMBED_POSTMETA_KEYS = ['_nectar_video_embed', 'video_post_url', 'Tm_video_url', '_format_video_embed']

    # sections
    PUBLISH_TO_FRONTPAGE = True
    ALLOW_UNCATEGORIZED = False

    STATUS_MAP = {
        'publish': 'post',
        'private': 'draft',
        'draft': 'draft',
        'pending': 'draft',
        'trash': None,
    }

    def __init__(self, api, authors_manager, sections_manager, attachments_manager):
        self.authors = authors_manager
        self.attachments = attachments_manager
        self.sections = sections_manager
        self.api = api

    def _build_base_entry(self):
        entry = {
            'roar_specific_data': {},
            'sections': [],
            'tags': [],
        }
        return entry

    def build_entry(self, item):
        entry = self._build_base_entry()
        for rm_field, (wp_field, parse_func) in self.primitive_mapping.items():
            entry[rm_field] = parse_func(item[wp_field])
        entry['status'] = self.get_status(item)
        entry['tags'] = self.get_tags(item)
        entry['sections'] = self.get_sections(item)
        entry['roar_author_ids'] = self.get_roar_author_ids(item)
        entry['roar_specific_data']['original_item'] = item
        meta = self.build_meta(item['meta'])
        entry['roar_specific_data']['meta'] = meta
        entry.update(self.get_dates(item))
        entry.update(self.get_lead_image(meta))
        # entry.update(self.get_meta_embeds(meta))
        entry['body'] = self.prepare_body(entry['body'])
        return entry

    def prepare_body(self, body):
        # TODO: body processing
        return body

    def publish_entry(self, entry):
        # filter fields
        # check dates for future posts
        # publish post/draft
        # return post
        status = entry.pop('status')
        response = self.api.create_draft(**entry)
        if status == 'post':
            self.api.publish_draft(response['id'])
        return response

    def postpublish(self, post):
        # TODO: create redirects for current slug and for old slugs
        return post

    def build_meta(self, item_meta):
        meta = collections.defaultdict(list)
        for k, v in item_meta:
            meta[k].append(v)
        return meta

    def get_status(self, item):
        if item['password']:
            return 'draft'
        return self.STATUS_MAP[item['status']]

    def get_tags(self, item):
        categories = item['category']
        tags = []
        for cat in categories:
            if cat['domain'] == 'post_tag':
                tags.append(cat['text'])
        return tags

    def get_roar_author_ids(self, item):
        return []
        author_id = self.authors.get_by_key(item['creator'])
        return [author_id]

    def get_sections(self, item):
        categories = item['category']
        sections = []
        for cat in categories:
            if cat['domain'] == 'category':
                slug = cat['nicename']
                if slug == 'uncategorized' and not self.ALLOW_UNCATEGORIZED:
                    continue
                sections.append(self.sections.get_by_slug(slug))
        if self.PUBLISH_TO_FRONTPAGE:
            sections.append('Home')
        return sections

    def get_dates(self, item):
        created_ts = FieldHandlers.wp_pub_date(item['pub_date'])
        response = {'created_ts': created_ts}
        # TODO: check for scheduling
        return response

    # def get_meta_embeds(self, meta):
    #     for field_name in self.EMBED_POSTMETA_KEYS:
    #         if field_name in meta:
    #             value = meta[field_name][0]
    #             if not value:
    #                 continue
    #             embed = get_embed(value)
    #             if embed:
    #                 return {
    #                     'video': embed.get_embed_url(),
    #                     'type': 'video',
    #                 }
    #             else:
    #                 p = urlparse.urlparse(value)
    #                 if p.path.endswith(('.mp4', '.m4p', '.webm', '.flv')):
    #                     return {
    #                         'video': value,
    #                         'type': 'video',
    #                     }
    #     return {}

    def get_lead_image(self, meta):
        for field_name in self.IMAGE_POSTMETA_KEYS:
            if field_name in meta:
                thumb_id = int(meta[field_name][0])
                image_info = self.attachments.get_image_info_by_id(thumb_id)
                if image_info and 'id' in image_info:
                    response = {
                        'image_id': image_info['id'],
                        'type': 'image',
                    }
                    caption, credit = self.attachments.get_caption_and_credit(thumb_id)
                    if caption:
                        response['photo_caption'] = caption
                    if credit:
                        response['photo_credit'] = credit
                    return response
        return {}
