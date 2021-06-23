# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HinduItem(scrapy.Item):
    place = scrapy.Field()
    time_stamp = scrapy.Field()
    heading = scrapy.Field()
    news_description = scrapy.Field()
    page_link = scrapy.Field()

