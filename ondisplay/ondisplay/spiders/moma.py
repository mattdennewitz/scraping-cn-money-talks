# -*- coding: utf-8 -*-
import json

import pydash as pd

import scrapy

from ..items import ArtworkItem
from ..loaders import BaseLoader


class MomaSpider(scrapy.Spider):
    name = 'moma'
    allowed_domains = ['moma.org']
    start_urls = ['https://www.moma.org/artists/3787?locale=en']

    def parse(self, response):
        """Scrapes artist detail page for links, dispatches link fetching
        """

        painting_urls = response.css(
            '#works a.link--tile::attr(href)').extract()

        self.logger.warn('%s urls found', len(painting_urls))

        for url in painting_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_artwork)

    def parse_artwork(self, response):
        """Scrapes an individual artwork
        """

        loader = BaseLoader(ArtworkItem(), response=response)
        loader.add_value('museum_name', 'moma')

        # extract ld+json blob
        ld_blob = response.xpath(
            '//script[@type="application/ld+json" and contains(., "CreativeWork")]/text()'
        ).get()

        # parse linked data entry for this artwork
        ld = json.loads(ld_blob)

        # extract values from linked data
        loader.add_value('artist_name', pd.get(ld, 'creator.0.name'))
        loader.add_value('artwork_title', pd.get(ld, 'name'))
        loader.add_value('thumbnail_url', pd.get(ld, 'image.0'))

        # `.locations__item` exists when the item is on display
        # we could also infer from "On View" / "Not on View" text
        loader.add_xpath('on_display',
                         'boolean(//li[@class="locations__item"])')

        yield loader.load_item()
