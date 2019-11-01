import lxml.etree


class DefaultXmlParser:
    @classmethod
    def parse(cls, content):
        return lxml.etree.fromstring(content)
