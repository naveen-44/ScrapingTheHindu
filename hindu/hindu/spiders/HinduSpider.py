import scrapy
from ..items import HinduItem


class HinduSpider(scrapy.Spider):
    name = 'hindu'
    start_urls = [
        'https://www.thehindu.com/news/national/'
    ]

    def parse(self, response):

        items = HinduItem()

        story_cards = response.css('.Other-StoryCard')

        for card in story_cards:

            page_link = card.xpath('a/@href').extract()

            items['page_link'] = page_link

            yield items
