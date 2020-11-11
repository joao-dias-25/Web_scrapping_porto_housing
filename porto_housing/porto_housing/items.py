# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PortoHousingItem(scrapy.Item):
    # define the fields for your item here like:

    price = scrapy.Field()
    address = scrapy.Field()
    title = scrapy.Field()
    id = scrapy.Field()
    creation_date = scrapy.Field()
    modified_date = scrapy.Field()
    from_agency = scrapy.Field()
    agency = scrapy.Field()
    link = scrapy.Field()
    areau = scrapy.Field()
    areab = scrapy.Field()
    Empree = scrapy.Field()
    Tipolo = scrapy.Field()
    estado = scrapy.Field()
    wc = scrapy.Field()
    ano = scrapy.Field()
    certif = scrapy.Field()
    descricao = scrapy.Field()

