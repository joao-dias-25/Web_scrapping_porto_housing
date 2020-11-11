import scrapy
from ..items import PortoHousingItem
import re

class PortoHousingSpider(scrapy.Spider):
    name = 'imovirtual'
    start_urls = [
        'https://www.imovirtual.com/comprar/apartamento/?locations%5B0%5D%5Bregion_id%5D=13&locations%5B0%5D%5Bsubregion_id%5D=190&locations%5B0%5D%5Bcity_id%5D=13643794&locations%5B1%5D%5Bregion_id%5D=13&locations%5B1%5D%5Bsubregion_id%5D=190&locations%5B1%5D%5Bcity_id%5D=13643793&locations%5B2%5D%5Bregion_id%5D=13&locations%5B2%5D%5Bsubregion_id%5D=190&locations%5B2%5D%5Bcity_id%5D=13643786&locations%5B3%5D%5Bregion_id%5D=13&locations%5B3%5D%5Bsubregion_id%5D=190&locations%5B3%5D%5Bcity_id%5D=13643779&locations%5B4%5D%5Bregion_id%5D=13&locations%5B4%5D%5Bsubregion_id%5D=190&locations%5B4%5D%5Bcity_id%5D=13643778'
    ]
    def parse(self, response):


        offer_items = response.css("div.offer-item-details")
        offer_links = offer_items.css('h3 a::attr(href)').getall()


        yield from response.follow_all(offer_links, self.parse_house)


        # Find next page and rerun this method

        next_page = response.css('li.pager-next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)

    def parse_house(self, response):
        """Parse information found on house description page."""
        items = PortoHousingItem()

        link_casa=response.css('link::attr(href)').extract()[1]
        title = response.css('h1.css-1ld8fwi::text').extract()
        address = response.css('a.css-1dnl7g2::text').extract()
        price = response.css('div.css-1vr19r7::text').extract()[0]
        id = response.css('div.css-kos6vh::text').extract()[0]
        creation_date = response.css('div.css-lh1bxu::text').extract()[0]
        modified_date = response.css('div.css-lh1bxu::text').extract()[1]
        from_agency = response.css('.css-16hwbg6::text').extract()
        agency = response.css('.css-zkkfhr-Aa strong::text').extract()
        descricao = "".join(response.css('.css-i6f3ud::text').extract())
        propriedades = response.css('.css-otm6a-Fe li').extract()

        for carac in propriedades:
            prop = carac.split(":",1)
            if prop[0][4:10] == 'Área ú':
                items['areau'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Área b':
                items['areab'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Empree':
                items['Empree'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Tipolo':
                items['Tipolo'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Casas ':
                items['wc'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Condiç':
                items['estado'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Ano de':
                items['ano'] = prop[1][9:-14]
            elif prop[0][4:10] == 'Certif':
                items['certif'] = prop[1][9:-14]


        items['price'] = price
        items['title'] = title
        items['address'] = address
        items['id'] = id
        items['creation_date'] = creation_date
        items['modified_date'] = modified_date
        items['from_agency'] = from_agency
        items['agency'] = agency
        items['link'] = link_casa
        items['descricao'] = descricao


        yield items