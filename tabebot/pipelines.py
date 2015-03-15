# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import json
from collections import defaultdict

from scrapy import signals
from scrapy.contrib.exporter import BaseItemExporter
from scrapy.exceptions import DropItem
from scrapy.xlib.pydispatch import dispatcher

from tabebot.items import BusinessItem, ReviewItem, UserItem


class PrettyFloat(float):
    '''
    Used to format floats in json
    http://stackoverflow.com/a/1733105
    '''
    def __repr__(self):
        return '%.2g' % self


def convert_to_utf8(json_obj):
    '''
    Converts simple json python representations to utf-8 recursively.

    Refer to:
    - http://stackoverflow.com/a/13105359
    - http://stackoverflow.com/q/18337407
    '''
    if isinstance(json_obj, dict):
        return dict((convert_to_utf8(key), convert_to_utf8(value))
                    for key, value in json_obj.iteritems())
    elif isinstance(json_obj, list):
        return [convert_to_utf8(element) for element in json_obj]
    elif isinstance(json_obj, unicode):
        return json_obj.encode('utf-8')
    elif isinstance(json_obj, float):
        return PrettyFloat(json_obj)
    else:
        return json_obj


class UnicodeJsonLinesItemExporter(BaseItemExporter):
    '''
    Prints out JSON in utf8 symbols, not their code points.
    Refer to https://groups.google.com/forum/#!topic/scrapy-users/rJcfSFVZ3O4
    '''
    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.encoder = json.JSONEncoder(ensure_ascii=False,
                                        separators=(',', ':'),
                                        **kwargs)

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(self.encoder.encode(convert_to_utf8(itemdict)) + '\n')


def item_type(item):
    '''
    Converts an `Item` to its string representation.
    Example: ReviewItem => review
    '''
    return type(item).__name__.replace('Item', '').lower()


class RemoveDuplicatesPipeline(object):
    def __init__(self):
        self.seen_items = defaultdict(set)

    def process_item(self, item, spider):
        if (isinstance(item, BusinessItem) or isinstance(item, ReviewItem)
                or isinstance(item, UserItem)):
            what = item_type(item)
            key = '{0}_id'.format(what)
            value = item[key]
            if value in self.seen_items[what]:
                raise DropItem('Duplicate {0} found: {1}'.format(what, item))
            else:
                self.seen_items[what].add(value)
                return item


# Shamelessly copied from http://stackoverflow.com/q/12230332
class MultiJsonLinesItemPipeline(object):
    save_types = ['review', 'business', 'user']

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        self.files = dict((name, open(name + '.json', 'w+b'))
                          for name in self.save_types)
        self.exporters = dict((name, UnicodeJsonLinesItemExporter(self.files[name]))
                              for name in self.save_types)
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.save_types):
            self.exporters[what].export_item(item)
        return item
