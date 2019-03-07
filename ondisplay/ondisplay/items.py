# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtworkItem(scrapy.Item):
    museum_name = scrapy.Field()
    artist_name = scrapy.Field()
    artwork_title = scrapy.Field()
    thumbnail_url = scrapy.Field()
    on_display = scrapy.Field()
