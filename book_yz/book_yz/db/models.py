# -*- coding: utf-8 -*-
import datetime

__author__ = 'zhougy'
__date__ = '2018/12/19 上午9:59'

'''
自定义orm业务模型类
'''

from book_yz.db.mysql_helper import MySQLORMHelper, Base

from sqlalchemy import Column, String, Integer, ForeignKey, Text, Float, Time, DateTime
import json


class Book(Base):
    __tablename__ = "book"
    # 书籍信息表
    book_id = Column(Integer, primary_key=True)
    book_name = Column(String(300))
    book_num = Column(String(100))
    book_class = Column(String(100))
    book_text = Column(Text)
    is_delete = Column(Integer, default=False)
    create_time = Column(DateTime, default=datetime.datetime.now())

    def __str__(self):
        res_dict = dict(
            book_id=self.book_id,
            book_name=self.book_name,
            book_num=self.book_num,
            book_class=self.book_class,
            book_text=self.book_text,
            is_delete=self.is_delete,
            create_time=self.create_time,

        )
        return json.dumps(res_dict)


class BookImg(Base):
    __tablename__ = "img"
    # 书籍图片表
    img_id = Column(Integer, primary_key=True)
    book_num = Column(String(100))
    book_img1 = Column(String(500))
    book_img2 = Column(String(500))
    book_img3 = Column(String(500))
    book_details_img = Column(String(500))
    is_delete = Column(Integer, default=False)
    create_time = Column(DateTime, default=datetime.datetime.now())

    def __str__(self):
        res_dict = dict(
            book_img1=self.book_img1,
            book_img2=self.book_img2,
            book_img3=self.book_img3,
            book_num=self.book_num,

            book_details_img=self.book_details_img,
            is_delete=self.is_delete,
            create_time=self.create_time,

        )
        return json.dumps(res_dict)


class Books(Base):
    __tablename__ = "sheet1"
    # 书籍图片表
    id = Column(Integer, primary_key=True)
    book_name = Column(String(500))
    book_num = Column(String(100))

    def __str__(self):
        res_dict = dict(
            id=self.id,
            book_name=self.book_name,
            book_num=self.book_num,

        )
        return json.dumps(res_dict)


def synchronous():
    minst = MySQLORMHelper()
    session = minst.create_session()
    return (minst, session)


if __name__ == "__main__":
    synchronous()
