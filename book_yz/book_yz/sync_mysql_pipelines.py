# -*- coding: utf-8 -*-


__author__ = 'zhougy'
__date__ = '2018/12/25 上午10:00'

from book_yz.db.models import *

from book_yz.db.models import synchronous

(minst, session) = synchronous()

from book_yz.items import *


class SyncMySQLBookPipeLine(object):

    def process_item(self, item, spider):
        '''
        :param item:  item是从spiders通过yield发射过来的对象
        :param spider:  spider是指的不同爬虫 （spider.name）
        :return:
        '''
        try:
            item_name = item.get_name()
            if item_name == "BooksYzItem":
                book = Book(
                            book_name=item['book_name'],
                            book_num=item['book_num'],
                            book_class=item["book_class"],
                            book_text=item["book_text"],
                            is_delete=item["is_delete"],
                            create_time=item["create_time"],
                            )
                minst.add_records(session, book)
            elif item_name == "BooksImgeYzItem":
                book_img = BookImg(
                    book_num=item['book_num'],
                    book_img1=item['book_img1'],
                    book_img2=item['book_img2'],
                    book_img3=item['book_img3'],

                    book_details_img=item['book_details_img'],
                    is_delete=item["is_delete"],
                    create_time=item["create_time"],
                )
                minst.add_records(session, book_img)

        except Exception as e:
            print(f"MySQLBookPipeLine:process_item has error: {e}")
        # return item
        finally:
            return item
