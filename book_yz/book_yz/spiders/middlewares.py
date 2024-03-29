# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.webdriver import ActionChains


class BookYzSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BookYzDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


'''
动态UserAgent代理
'''
import logging
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from book_yz.settings import USER_AGENT_LIST


class RotateUserAgentMiddleware(UserAgentMiddleware):
    '''
    用户代理中间件（处于下载中间件位置）
    UA代理池属于下载中间件，在下载中间件中的process_request的时候往request请求头部加入User-Agent
    从列表中随机选取一个ua
    '''

    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)
            # print(f"User-Agent:{user_agent} is using.")
        return None

    def process_exception(self, request, exception, spider):
        error_info = f"spider:{spider.name} RotateUserAgentMiddleware has error with {exception}"
        print(error_info)
        logging.error(error_info)


from book_yz.settings import IP_PROXY_LIST


class MyIPProxyMiddleWare(object):
    '''
    ip 代理池
    '''

    def process_request(self, request, spider):
        # 从list中选取IP，设置到request
        ip_proxy = random.choice(IP_PROXY_LIST)
        if ip_proxy:
            request.meta['proxies'] = ip_proxy  # 此处关键字proxies不能错
            # print(f"IP_PROXY:{ip_proxy}")

    def process_exception(self, request, exception, spider):
        error_info = f"spider:{spider.name} MyIPProxyMiddleWare has error with {exception}"
        print(error_info)
        logging.error(error_info)


class SeleniumMiddleware:
    def process_request(self, request, spider):
        # if spider.name == 'amazon_spider' and request.meta.get("type", None) == "amazon":
        #     spider.driver.get(request.url)
        #     time.sleep(3)
        #     js = "window.scrollTo(0, 10000)"
        #     spider.driver.execute_script(js)
        #     time.sleep(2)
        #     spider.driver.find_element_by_xpath(
        #         f"//div[@role='section'][2]/button").click()
        # if spider.name == 'book_spider' and request.meta.get('type', None) == "details_item":
        #     spider.driver.get(request.url)
        #     time.sleep(2)
        #
        #     button_list = []
        #     for i in range(6, 11):
        #         start_button = spider.driver.find_element_by_xpath(
        #             f"//ul[@id='main-img-slider']/li[{i}]/a/img")
        #         button_list.append(start_button)
        #     for j in range(len(button_list) - 1):
        #         spider.driver.execute_script("arguments[0].scrollIntoView();", button_list[j])
        #         time.sleep(2)
        #         ActionChains(spider.driver).move_to_element(button_list[j]).perform()
        #         time.sleep(2)
        #         # 将鼠标移动到移动的标签位置
        #         if j != 5:
        #             ActionChains(spider.driver).move_to_element(button_list[j + 1]).perform()
        #             time.sleep(2)
        # for j in range(1, 9):
        #     start_button = spider.driver.find_element_by_xpath(
        #         f"//div[@class='newsdata_nav']/ul/li[{j}]")
        #
        #     button_list.append(start_button)
        #
        # for i in range(8):
        #     # 将页面拉到底部
        #     js = "window.scrollTo(0, 10000)"
        #     spider.driver.execute_script(js)
        #     time.sleep(2)
        #     js = "window.scrollTo(10000, 18000)"
        #     spider.driver.execute_script(js)
        #     time.sleep(2)
        #     js = "window.scrollTo(18000, 23000)"
        #     spider.driver.execute_script(js)
        #     time.sleep(3)
        #     # 不能超过列表索引长度
        #     if i != 7:
        #         spider.driver.execute_script("arguments[0].scrollIntoView();", button_list[i])
        #         time.sleep(3)
        #         ActionChains(spider.driver).move_to_element(button_list[i]).perform()
        #         time.sleep(3)
        #         # 将鼠标移动到移动的标签位置
        #         ActionChains(spider.driver).move_to_element(button_list[i + 1]).perform()
        #         time.sleep(5)
        #     else:
        #         # 必须在移动一次标签上一次标签的内容才能显示
        #         spider.driver.execute_script("arguments[0].scrollIntoView();", button_list[i])
        #         time.sleep(3)
        #         ActionChains(spider.driver).move_to_element(button_list[i]).perform()
        #         time.sleep(3)
        #         ActionChains(spider.driver).move_to_element(button_list[i - 1]).perform()
        #         time.sleep(5)
        if spider.name == 'yz_spider' and request.meta.get("type", None) == "dangdang":
            spider.driver.get(request.url)
            time.sleep(3)
            spider.driver.find_element_by_id("key_S").send_keys("Python")
            spider.driver.find_element_by_xpath(
                f"//div[@class='logo_line']/div[2]/form/input[9]").click()

        # if spider.name == 'yz_spider' and request.meta.get("type", None) == "book_details ":
        #     spider.driver.get(request.url)
        #     time.sleep(3)


        return HtmlResponse(
            url=spider.driver.current_url,
            body=spider.driver.page_source,
            request=request,
            encoding="utf-8",
        )


