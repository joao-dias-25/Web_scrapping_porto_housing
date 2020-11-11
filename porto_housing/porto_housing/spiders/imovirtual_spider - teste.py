import scrapy
from ..items import PortoHousingItem

class PortoHousingSpider(scrapy.Spider):
    name = 'imovirtual'
    start_urls = [
        'https://www.imovirtual.com/comprar/predio/porto/?search%5Bregion_id%5D=13&search%5Bsubregion_id%5D=190'
    ]
    def parse(self, response):

        items = PortoHousingItem()

        offer_items = response.css("div.offer-item-details")

        for offer in offer_items:

            title = offer.css('span.offer-item-title::text').extract()[0]
            price = offer.css('li.offer-item-price::text').extract()[0].replace(' ','')

            format = offer.css('.offer-item-rooms::text').extract()
            area = offer.css('.offer-item-area::text').extract()[0]
            #params = response.css('.hidden-xs li::text').extract()
            #type = response.css('span.hidden-xs::text').extract()
            #local = response.css('p.text-nowrap::text').extract()

            items['price'] = price
            items['area'] = area
            items['format'] = format
            items['title'] = title

            yield items


        next_page = response.css('li.pager-next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)
