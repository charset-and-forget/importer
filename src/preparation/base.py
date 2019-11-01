import collections
import glob

import lxml.etree

import app.preparation.flows
import app.preparation.wp.parsers as wp_parsers
import app.preparation.wp.extractors as wp_extractors


class PreparatorBase:
    extractors = None
    flow_cls = app.preparation.flows.DumbFlow
    parser_cls = None
    # supported_groups = ['posts', 'authors', 'sections', 'media', 'guest_authors']

    @classmethod
    def process(cls, source, destination=None):
        response = collections.defaultdict(dict)

        for content in cls.flow_cls.iterate_from_source(source):
            try:
                parsed_content = cls.parser_cls.parse(content)
            except lxml.etree.XMLSyntaxError:
                prepared_content = cls._prepare_content(content)
                try:
                    parsed_content = cls.parser_cls.parse(prepared_content)
                except:
                    with open('error.xml', 'wb') as f:
                        f.write(prepared_content)
                    raise
            for extractor in cls.extractors:
                for group, key, item in extractor.iterate(parsed_content):
                    response[group][key] = item

        # flattening response:
        response = {
            k: v.values()
            for k, v in response.items()
        }
        return cls.flow_cls.move_to_destination(response, destination)

    @classmethod
    def _prepare_content(cls, content):
        broken_symbols = [
            b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06',
            b'\x08', b'\x0B', b'\x0C', b'\x10', b'\x11', b'\x13', b'\x14',
            b'\x17', b'\x18', b'\x19', b'\x1C', b'\x1D', b'\x1E',
        ]
        for i in broken_symbols:
            content = content.replace(i, b'')
        return content


class WpPreparator(PreparatorBase):
    extractors = [wp_extractors.SectionExtractor, wp_extractors.ItemExtractor, wp_extractors.AuthorExtractor]
    flow_cls = app.preparation.flows.FileFlow
    parser_cls = wp_parsers.DefaultXmlParser
