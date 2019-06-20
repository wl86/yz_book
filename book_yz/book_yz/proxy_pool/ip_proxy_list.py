# -*- coding: utf-8 -*-

import requests

import threading

from threading import Lock

import queue

# from BookToscrape.settings import R, IP_PROXY_WRITE_TYPE

g_lock = Lock()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def store_file(ip_port):
    with open("proxy_list.txt", "a+", encoding="utf-8") as f:
        f.write(f"{ip_port}\n")


# def store_redis(ip_port):
# 	R.sadd("ip_port_set", ip_port)     #数据存入集合
# 	R.expire("ip_port_set", 24*60*60)  #超时时间

#
# STORE_MAP = {
# 	'file':store_file,
# 	'redis':store_redis,
# }


def fetch_web_data(url, proxies=None, timeout=10):
    try:
        r = requests.get(url, headers=headers, timeout=timeout, proxies=proxies)
        return r.text
    except Exception as e:
        print(f"fetch_web_data has error with url:{url}, error:{e}")
        return None


class FetchProxyListThread(threading.Thread):
    '''
    从http://www.thebigproxylist.com/members/proxy-api.php?output=all&user=list&pass=8a544b2637e7a45d1536e34680e11adf
    网络接口中下载代理数据
    '''

    def __init__(self, url, mq):
        threading.Thread.__init__(self)
        self.__url = url
        self.__mq = mq

    def run(self):
        '''
        下载接口数据，保存到mq
        :return:
        '''
        data = fetch_web_data(self.__url)
        ip_pool_list = data.split("\n")
        [self.__mq.put(ip_pool.split(",")[0]) for ip_pool in ip_pool_list]


CHECK_URL = "http://httpbin.org/get?x=2&y=4"


class IPProxyCheckThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.__queue = queue

    def run(self):
        global g_lock
        while True:
            ip_port = None
            try:
                ip_port = self.__queue.get(timeout=10)
            except Exception as e:
                break
            print(f"current data is {ip_port}")
            proxies = {
                'http': ip_port,
            }
            data = fetch_web_data(CHECK_URL, proxies=proxies, timeout=5)
            if data == None:
                print(f"当前IP对 {ip_port} 校验不成功，丢弃！")
                continue
            print(f"当前IP对 {ip_port} 校验成功，可用！")

            # g_lock.acquire()
            store_file(ip_port)
    # STORE_MAP[IP_PROXY_WRITE_TYPE](ip_port)

    # g_lock.release()


def process():
    mq = queue.Queue()

    url = "http://www.thebigproxylist.com/members/proxy-api.php?output=all&user=list&pass=8a544b2637e7a45d1536e34680e11adf"
    fth = FetchProxyListThread(url, mq)

    thread_num = 10
    thread_list = []
    for i in range(thread_num):
        t = IPProxyCheckThread(mq)
        thread_list.append(t)

    fth.start()
    [th.start() for th in thread_list]

    fth.join()
    [th.join() for th in thread_list]

    print("all work has done.")


if __name__ == "__main__":
    process()
