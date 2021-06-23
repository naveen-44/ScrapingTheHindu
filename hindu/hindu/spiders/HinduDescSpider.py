import scrapy
from ..items import HinduItem
import csv


class HinduDescSpider(scrapy.Spider):
    name = 'hinduDesc'
    with open('pagelinks.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    start_urls = []
    for i, row in enumerate(data):
        if i > 1:
            start_urls.append(row[2])
    print(start_urls[:5])

    def parse(self, response):

        items = HinduItem()
        title = response.css('title::text').extract()[0]
        title = title.replace(' - The Hindu', '')
        title = title.replace('\n', '')

        link = str(response).replace('<200 ', '')
        link = link.replace('>', '')

        descriptions = response.css('#artmeterinlinewrap+ div p::text').extract()
        para = ''
        for description in descriptions:
            para += description
            if para[-1] == '.':
                para += ' '

        place = response.css('.ksl-time-stamp:nth-child(1)::text').extract()[0].replace("\n", "")
        place = place.replace(",", "")

        time_stamp = response.css('.ksl-time-stamp none ::text').extract()[0].replace("\n", "")

        items['news_description'] = para
        items['heading'] = title
        items['page_link'] = link
        items['place'] = place
        items['time_stamp'] = time_stamp

        yield items
