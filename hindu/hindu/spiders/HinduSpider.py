import scrapy
from ..items import HinduItem


class HinduSpider(scrapy.Spider):
    name = 'hindu'
    page_number = 2
    start_urls = ['https://www.thehindu.com/news/national/']

    def parse(self, response):
        items = HinduItem()
        story_cards = response.css('.Other-StoryCard')

        # Extracting the link from every story card
        for card in story_cards:
            page_link = card.xpath('a/@href').extract()
            items['page_link'] = page_link
            yield items

        curr_page = 'https://www.thehindu.com/news/national/?page='
        next_page = curr_page + str(HinduSpider.page_number) + '/'

        if HinduSpider.page_number < 20:
            HinduSpider.page_number += 1

            yield response.follow(
                next_page,
                callback=self.parse,
                dont_filter=True
            )
