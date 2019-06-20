# -*- coding: utf-8 -*-  

'''
web浏览器配置文件
走有头，无头浏览器
'''
#
# from selenium import webdriver
#
# def create_bs_driver(type="firefox", headless=False):
# 	'''
# 	:param type:
# 	:param headless:  是否为无头浏览器，True---无头，  False---有头
# 	:return:
# 	'''
# 	if type == "firefox":   #火狐浏览器
# 		firefox_opt = webdriver.FirefoxOptions()
# 		firefox_opt.add_argument("--headless") if headless else None
# 		driver = webdriver.Firefox(firefox_options=firefox_opt)
# 	elif type == "chrome":  #谷歌浏览器
# 		chrome_opt = webdriver.ChromeOptions()
# 		chrome_opt.add_argument("--headless") if headless else None
# 		driver = webdriver.Chrome(chrome_options=chrome_opt)
# 	else:
# 		return None
# 	return driver

'''
web浏览器配置文件
走有头，无头浏览器
'''

from selenium import webdriver
import random
from selenium.webdriver.common.action_chains import *


from book_yz.settings import USER_AGENT_LIST, IP_PROXY_LIST


def create_bs_driver(type="firefox", headless=False):
    '''
    :param type:
    :param headless:  是否为无头浏览器，True---无头，  False---有头
    :return:
    '''


    if type == "firefox":  # 火狐浏览器
        firefox_opt = webdriver.FirefoxOptions()
        # 设置selenium ua代理池
        user_agent = f"--user-agent={random.choice(USER_AGENT_LIST)}"
        firefox_opt.add_argument(user_agent)
        # 设置selenium的ip代理池
        ip_agent = f"--proxy-server=http://{random.choice(IP_PROXY_LIST)}"
        firefox_opt.add_argument(ip_agent)
        firefox_opt.add_argument("--headless") if headless else None
        driver = webdriver.Firefox(firefox_options=firefox_opt)
    elif type == "chrome":  # 谷歌浏览器
        chrome_opt = webdriver.ChromeOptions()
        # 设置selenium ua代理池
        user_agent = f"--user-agent={random.choice(USER_AGENT_LIST)}"
        chrome_opt.add_argument(user_agent)
        # 设置selenium的ip代理池
        ip_agent = f"--proxy-server=http://{random.choice(IP_PROXY_LIST)}"
        chrome_opt.add_argument(ip_agent)
        chrome_opt.add_argument("--headless") if headless else None
        driver = webdriver.Chrome(chrome_options=chrome_opt)
    else:
        return None
    return driver
