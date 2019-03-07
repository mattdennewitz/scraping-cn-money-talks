# -*- coding: utf-8 -*-
import scrapy

from ..items import ArtworkItem
from ..loaders import BaseLoader


class ArticSpider(scrapy.Spider):
    name = 'artic'
    allowed_domains = ['artic.edu']
    start_urls = ['https://www.artic.edu/artists/16367/agnes-martin']

    def parse(self, response):
        """Scrapes artist detail page for links, dispatches link fetching
        """

        painting_urls = response.xpath(
            '//main[@id="content"]/ul[1]/'  # first <ul> child
            'li[contains(@itemtype, "CreativeWork")]/'  # creative works only
            'a[@itemprop="url"]/@href'  # just the link url
        ).extract()

        self.logger.warn('%s urls found', len(painting_urls))

        for url in painting_urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_artwork)

    def parse_artwork(self, response):
        """Scrapes an individual artwork
        """

        loader = BaseLoader(ArtworkItem(), response=response)
        loader.add_value('museum_name', 'aic')

        # extract artist name
        # note: this is not resiliant to, say, the greek collection
        #       where authors are unknown
        loader.add_xpath(
            'artist_name',
            '//dl[@id="dl-artwork-details"]/dd[@itemprop="creator"]/span/a/text()'
        )

        # extract artwork title
        loader.add_xpath(
            'artwork_title',
            '//dl[@id="dl-artwork-details"]/dd[@itemprop="name"]/*/text()')

        # extract thumbnail url
        loader.add_xpath('thumbnail_url',
                         '//meta[@property="og:image"]/@content')

        # extract on display status
        # note: this is an assumption that would change given
        #       a redesign or language change
        loader.add_xpath(
            'on_display',
            'boolean(//main[@id="content"]//h2[contains(., "On View")])')

        yield loader.load_item()
