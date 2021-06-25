import scrapy
from ..items import HinduItem
import csv


def loadURLs():
    # Opens the pagelinks.csv and reads the links and saves it in
    # urls and returns the list of urls to start the spider with
    urls = []
    with open('pagelinks.csv', newline='') as csvFile:
        data = list(csv.reader(csvFile))
    for i, row in enumerate(data):
        if i > 1:                       # ignores the heading of the csv file
            urls.append(row[2])         # row[2] contains the page links
    return urls


class HinduDescSpider(scrapy.Spider):
    name = 'hinduDesc'
    start_urls = loadURLs()

    def parse(self, response):

        def cleanThePlace(unclean_place):
            # removing newline and unwanted comma at the end
            cleaned_place = unclean_place.replace("\n", "")
            cleaned_place = cleaned_place.replace(",", "")
            return cleaned_place

        def cleanTheTime(unclean_time):
            # just removing the newline in the string
            clean_time = unclean_time.replace("\n", "")
            return clean_time

        def makeDescToPara(descriptions):
            # descriptions have multiple sentences some ending with period and
            # some ending with blank space which is all combined into just one
            # paragraph and if the line ends with a period, a space is added
            paragraph = ''
            for description in descriptions:
                paragraph += description
                if paragraph[-1] == '.':
                    paragraph += ' '
            return paragraph

        def cleanTheTitle(unclean_title):
            # every title contains "-the hindu" and a newline in between which
            # is removed from the string
            cleaned_title = unclean_title.replace(' - The Hindu', '')
            cleaned_title = cleaned_title.replace('\n', '')
            return cleaned_title

        def cleanTheLink(unclean_response):
            # all the links are as <200 link > hence, the <> and 200 in the link
            # are removed from the response
            cleaned_link = str(unclean_response).replace('<200 ', '')
            cleaned_link = cleaned_link.replace('>', '')
            return cleaned_link

        items = HinduItem()

        # EXTRACTING the values from the response
        title = response.css('title::text').extract()[0]
        descriptions = response.css('#artmeterinlinewrap+ div p::text').extract()
        place = response.css('.ksl-time-stamp:nth-child(1)::text').extract()[0]
        time_stamp = response.css('.ksl-time-stamp none ::text').extract()[0]

        # CLEANING the extracted values
        link = cleanTheLink(response)
        title = cleanTheTitle(title)
        para = makeDescToPara(descriptions)
        place = cleanThePlace(place)
        time_stamp = cleanTheTime(time_stamp)

        # APPENDING the values into the item
        items['news_description'] = para
        items['heading'] = title
        items['page_link'] = link
        items['place'] = place
        items['time_stamp'] = time_stamp

        yield items
