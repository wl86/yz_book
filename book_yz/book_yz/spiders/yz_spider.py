# -*- coding: utf-8 -*-
import datetime
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from book_yz.items import *
from book_yz.utils.bshead import create_bs_driver
from book_yz.sync_mysql_pipelines import session
from book_yz.db.models import *

num_list = session.query(Books.book_num).all()

# num_list = ["9787111603665","9787115428028"]
img1 = ''
img2 = ''
img3 = ''


class YzSpiderSpider(CrawlSpider):
    name = 'yz_spider'
    allowed_domains = ['www.dangdang.com']
    start_urls = ['http://www.dangdang.com/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def __init__(self):
        CrawlSpider.__init__(self, self.name)
        self.driver = create_bs_driver()

        self.driver.set_page_load_timeout(20)
        self.num = ''

    def __del__(self):

        self.driver.quit()

    def start_requests(self):
        for num in num_list[11:13]:
            if len(num[0]) > 12:
                self.num = num[0]
                for url in self.start_urls:
                    r = Request(url=url, dont_filter=True, callback=self.parse_item,
                                meta={'type': 'home', 'num': self.num})
                    yield r

    def parse_item(self, response):
        '''
        搜索到的书籍列表,从中获取第一个书籍url
        :param response:
        :return:
        '''
        # 书籍的Url

        book_url = response.xpath("//div[2]/div[@id='search_nature_rg']/ul/li[1]/a/@href").extract_first()

        p = Request(url=book_url, dont_filter=True, callback=self.details_item2, meta={"type": "details2"})
        yield p

        q = Request(url=book_url, dont_filter=True, callback=self.details_item3, meta={"type": "details3"})
        yield q

        y = Request(url=book_url, dont_filter=True, callback=self.details_item,
                    meta={"type": "details"})
        yield y

    def details_item2(self, response):

        book_img2 = response.xpath(f"//div[@class='pic_info']/div/a/img/@src").extract_first()
        img2 = book_img2

    def details_item3(self, response):
        book_img3 = response.xpath(f"//div[@class='pic_info']/div/a/img/@src").extract_first()
        img3 = book_img3

    def details_item(self, response):
        '''
        解析获取书籍信息
        :param reponse:
        :return:
        '''
        # 书籍名称
        book_name = response.xpath("//div[@class='name_info']/h1/@title").extract_first()
        # 书籍编码
        book_str1 = response.xpath("//ul[@class='key clearfix']/li[5]/text()").extract_first()
        book_str2 = response.xpath("//div[@id='detail_describe']/ul/li[1]/text()").extract_first()
        if book_str1 == None:
            book_num = book_str2.split("：")[1]
        else:
            book_num = book_str1.split("：")[1]

        # 书籍图片列表
        book_img1 = response.xpath(f"//div[@class='pic_info']/div/a/img/@src").extract_first()
        # print(book_img1, "1")
        img1 = book_img1
        # 书籍详情图片
        book_details_img1 = response.xpath("//div[@id='feature']/div[2]/img[1]/@src").extract_first()
        # 书籍详情图片, 上一个可能没有
        book_details_img2 = response.xpath("//div[@class='descrip']/div/div/img/@src").extract_first()
        book_details_img3 = response.xpath("//div[@id='description']/div[2]/img[1]/@src").extract_first()
        book_details_img4 = response.xpath("//div[@class='descrip']/p/img/@src").extract_first()
        # 书籍一级分类

        book_class = response.xpath("//span[@class='lie']/a[2]/text()").extract_first()
        # 书籍在线阅读内容,是个列表
        book_c1 = response.xpath("//div[@id='content']/div[@class='descrip']/p/text()").extract_first()
        book_c2 = response.xpath("//div[@id='content']/div[@class='descrip']/text()").extract_first()

        book_text_list = response.xpath("//div[@id='extract']/div[2]/p/span/text()").extract()
        # 将书籍内容添加进空的字符串中
        book_text = ""
        if book_c1 == None:
            if book_c2 != None:
                for i in book_c2:
                    book_text += i
        else:
            for i in book_c1:
                book_text += i
        print(img1, "1", img2, "2", img3)
        # books = BooksYzItem(
        #     book_num=book_num,
        #     book_name=book_name,
        #     book_class=book_class,
        #     book_text=book_text,
        #     is_delete=1,
        #     create_time=datetime.datetime.now(), )
        # yield books
        # if len(self.img_list) == 1:
        #     self.img_list.append("null")
        # if len(self.img_list) == 2:
        #     self.img_list.append("null")
        # print(self.img_list)
        # if book_details_img1 == None:
        #     if book_details_img2 != None:
        #         book_details_img = book_details_img2
        #         book_imgs1 = BooksImgeYzItem(
        #             book_num=book_num,
        #             book_img1=self.img_list[0],
        #             book_img2=self.img_list[1],
        #             book_img3=self.img_list[2],
        #             is_delete=1,
        #             book_details_img=book_details_img,
        #             create_time=datetime.datetime.now(),
        #         )
        #
        #         yield book_imgs1
        #
        #
        #     else:
        #         if book_details_img3 != None:
        #             if book_details_img4 != None:
        #                 book_details_img = book_details_img4
        #                 book_imgs1 = BooksImgeYzItem(
        #                     book_num=book_num,
        #                     book_img1=self.img_list[0],
        #                     book_img2=self.img_list[1],
        #                     book_img3=self.img_list[2],
        #                     is_delete=1,
        #                     book_details_img=book_details_img,
        #                     create_time=datetime.datetime.now(),
        #                 )
        #
        #                 yield book_imgs1
        #
        #             else:
        #                 book_details_img = book_details_img3
        #                 book_imgs1 = BooksImgeYzItem(
        #                     book_num=book_num,
        #                     book_img1=self.img_list[0],
        #                     book_img2=self.img_list[1],
        #                     book_img3=self.img_list[2],
        #                     is_delete=1,
        #                     book_details_img=book_details_img,
        #                     create_time=datetime.datetime.now(),
        #                 )
        #
        #                 yield book_imgs1
        #
        #         else:
        #             book_details_img = book_details_img4
        #             book_imgs1 = BooksImgeYzItem(
        #                 book_num=book_num,
        #                 book_img1=self.img_list[0],
        #                 book_img2=self.img_list[1],
        #                 book_img3=self.img_list[2],
        #                 is_delete=1,
        #                 book_details_img=book_details_img,
        #                 create_time=datetime.datetime.now(),
        #             )
        #
        #             yield book_imgs1
        #
        # else:
        #     book_imgs1 = BooksImgeYzItem(
        #         book_num=book_num,
        #         book_img1=self.img_list[0],
        #         book_img2=self.img_list[1],
        #         book_img3=self.img_list[2],
        #         is_delete=1,
        #         book_details_img=book_details_img1,
        #         create_time=datetime.datetime.now(),
        #     )
        #
        #     yield book_imgs1
        #
