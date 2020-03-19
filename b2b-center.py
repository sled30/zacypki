#!/usr/bin/python
from selenium.webdriver import Firefox
# import requests
# from requests import Response
# from selenium import webdriver
from bs4 import BeautifulSoup
import re

uri = "https://www.b2b-center.ru"
urn = "/market/?f_keyword=автобус&searching=1&main_page_search=1&from=20#search-result"
url = uri + urn


def get_page(url):
    webdriver = "/home/sled/work/coding/parser/avtobus_1/lib/"
    driver = Firefox(webdriver)
    driver.get(url)
    data = driver.page_source
    driver.close()

    return data
def get_urn_advert(page):
    try:
        urn = re.findall(r'<tr><td><a href="(\/market\/.{10,}\/)"', page)

        return urn

    except Exception as e:
        print('get_urn_advert')
        print(e)
def get_advert_settings(url):
    page = get_page(url)
    print(page)

page = get_page(url)
urn_adverts = get_urn_advert(page)
for urn_advert in urn_adverts:
    url_advert = uri + urn_advert
    get_advert_settings(url_advert)
