# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookYzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BooksYzItem(scrapy.Item):
    book_num = scrapy.Field()
    book_name = scrapy.Field()
    book_class = scrapy.Field()
    book_text = scrapy.Field()
    is_delete = scrapy.Field()
    create_time = scrapy.Field()

    def get_name(self):
        return BooksYzItem.__name__


class BooksImgeYzItem(scrapy.Item):
    book_img1 = scrapy.Field()
    book_img2 = scrapy.Field()
    book_img3 = scrapy.Field()
    book_num = scrapy.Field()
    book_details_img = scrapy.Field()
    is_delete = scrapy.Field()
    create_time = scrapy.Field()

    def get_name(self):
        return BooksImgeYzItem.__name__
