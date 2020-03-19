#!/usr/bin/python
#from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# import requests
# from requests import Response
from selenium import webdriver

from bs4 import BeautifulSoup
import re
import time
import sqlite3

def get_page(url):
    options = Options()
    options.headless = True
#    webdriver = "/home/sled/work/coding/parser/avtobus_1/lib/"
    driver = webdriver.Firefox(options = options, executable_path=r'/home/sled/work/coding/parser/avtobus_1/lib/geckodriver')
#    driver = Firefox(webdriver)
    driver.get(url)
    data = driver.page_source
    driver.close()

    return data

def parse_first_page(page):
    try:

        first_date_advert = re.findall(r'<\/div><\/span><\/div><div data-\w{1}-[a-z,0-9]{8,9}.{178}Стартовая&nbsp;цена:.{63}(\d{1,6},.{0,2}&nbsp;руб).{100,}href=\"\/purchase\/\d{3,}\/order-info\".{30,}(\d{18}).{50,}Статус закупки:.{40,67}>(\D{4,})</div><!.{231}([^\d<,]{2,}).{4,}>([А-Я .-]{3,}).{30,}контракта: (\d{2}.\d{2}.\d{2}).{60,}href=\"(/purchase/\d{5,}/order-info)', page)
        return first_date_advert
    except Exception as e:
        print('parse_first_page')
        print(e)

def get_max_num_page(date):
    try:

        max_num_page = re.search(r'item cursor-pointer px13 last\">(\d{1,3})', date)

        return int(max_num_page[1])

    except Exception as e:
        print('get_max_num_page(date)')
        print(e)

def check_need_info(title):
    try:
        find = re.search(r'автобусы', title)
        if find:
            find = re.search(r'ремонтное', title)
            if find is None:
                return 1
        find = re.search(r'перевозка', title)
        if find:
            find = re.search(r'машины', title)
            if find is None:
                return 1
        find = re.search(r'транспорное', title)
        if find:
            find = re.search(r'спецтехники', title)
            if find is None:
                return 1
        find = re.search(r'транспорные' , title)
        if find:
            find = re.search(r'продажа', title)
            if find is None:
                return 1
        find = re.search(r'автобусов' , title)
        if find:
            find = re.search(r'специальный транспорт', title)
            if find is None:
                return 1
        find = re.search(r'микроавтобусы' , title)
        if find:
            find = re.search(r'грузов', title)
            if find is None:
                return 1
        find = re.search(r'транспортное сопровождение' , title)
        if find:
            find = re.search(r'промышленнных', title)
            if find is None:
                return 1
        find = re.search(r'транспортное обслуживание' , title)
        if find:
            find = re.search(r'отходов', title)
            if find is None:
                return 1
        find = re.search(r'транспорных услуг' , title)
        if find:
            find = re.search(r'страхование', title)
            if find is None:
                return 1
        find = re.search(r'транспортного средства' , title)
        if find:
            find = re.search(r'осмотр', title)
            if find is None:
                return 1
        find = re.search(r'микроавтобусов' , title)
        if find:
            find = re.search(r'техническое обслуживание', title)
            if find is None:
                return 1
        find = re.search(r'транспортировка' , title)
        if find:
            find = re.search(r'оборудование', title)
            if find is None:
                return 1
        find = re.search(r'перевозка сотрудников' , title)
        if find:
            find = re.search(r'технологическим', title)
            if find is None:
                return 1
        find = re.search(r'регулярные перевозки' , title)
        if find:
            find = re.search(r'грузоперевозки', title)
            if find is None:
                return 1
        find = re.search(r'транспортных средств' , title)
        if find:
            return 1

        find = re.search(r'доставка сотрудников' , title)
        if find:
            return 1

        find = re.search(r'детей' , title)
        if find:
            return 1

        find = re.search(r'оферта' , title)
        if find:
            return 1

    except Exception as e:
        print('Error check_need_info(title) ')
        print(e)
#    status = None

def get_advert_info(advert_page):

    url = "https://agregatoreat.ru" + advert_page[6]
    source_advert = get_page(url)

    advert_text = get_advert_text(source_advert)

    advert_type = get_advert_type(source_advert)

    createtion_date = get_creation_date(source_advert)
    end_advert_date = get_end_advert_date(source_advert)
    """ окончание падачи"""

    date_of_conclusion = get_date_of_conclusion(source_advert)
    """ Планируемая дата заключения"""
    region = get_region(source_advert)

    date = (advert_page[1], advert_page[2], advert_page[3], advert_page[4], advert_page[3], advert_text[0:49], advert_type, createtion_date, end_advert_date, date_of_conclusion, region, url)

    save_date(date)

def save_date(date):
    print(date[0])
    status = get_check_save_avert(date[0])
    print(status)
    if status == True:

        print('save')
        print(date, " \n")
        insert_agregator(date)
    #insert_agregator(date)
    else:
        print(date[0], " not saved")


def logic_work():

    uri = "https://agregatoreat.ru"
    urn = "/purchases/new/page/"
    base_page = str(1)
    link = uri + urn
    url = link + base_page

    try:
        source_index_page = get_page(url)
        if source_index_page:
            max_page = get_max_num_page(source_index_page)
            parse_date(source_index_page)
            for number in range(2, max_page):

                page = get_page(link + str(number))
                parse_date(page)

    except Exception as e:
        print(e)

def parse_date(source_index_page):

    first_date = parse_first_page(source_index_page)
    for date in first_date:

        status = check_need_info(date[3])
        if status is not None:
            get_advert_info(date)

def get_name_company(page):
    try:

        name_company = re.search(r'Наименование</div>.{170,179}\">([а-яА-Я \"-]{3,})<', page)



        if name_company[1] is None:
            name_company[1] = "No get date"


        return name_company[1]

    except Exception as e:
        print(e)

def get_advert_text(page):
    advert_text = re.search(r'Наименование закупки.{87}>(.{1,300})</div><!--', page)

    return advert_text[1]

def get_advert_type(page):
    advert_type = re.search(r'Тип закупки.{69}(.{10,100})</div><!', page)

    return advert_type[1]

def get_advert_terms_of_payment(source_advert):
    try:
        terms_of_payment = re.search(r'Условия оплаты.{10,100}\">([А-Яа-я ]{4,})', page)
        return terms_of_payment[1]

    except Exception as e:
        pass
def get_creation_date(source_advert):
    try:
        createtion_date = re.search(r'Дата и время размещения закупки.{10,70}>([\d.: ]{10,})<', source_advert)

        return createtion_date[1]
    except Exception as e:
        raise
def get_end_advert_date(source_advert):
    try:
        advert_end_date = re.search(r'Дата и время окончания подачи предложений.{10,70}\"\">([\d. :]{19})<', source_advert)


        return advert_end_date[1]
    except Exception as e:
        raise
def get_date_of_conclusion(source_advert):
    try:
        date_of_conclusion = re.search(r'Планируемая дата заключения контракта.{59,70}\"\">([\d. ]{8,10})', source_advert)

        return date_of_conclusion[1]
    except Exception as e:
        raise

def get_region(source_advert):
    try:
        region = re.search(r'Регион поставки.{20,100}\">([а-яА-Я .]{3,})<', source_advert)

        return region[1]
    except Exception as e:
        raise
def conn():
    connect = sqlite3.connect('data/storageDB') # 'data/mydb'
    return connect
def get_check_save_avert(number_advert):

    try:
        sql = "select `number_advert` from agregator where number_advert='{}'".format(number_advert)
        connect = conn()
        cur = connect.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        len_rows = len(rows)
        if len_rows == 0:
            return True
        else:
             return False

        connect.close

    except Exception as e:
        print(e)
    #    for num, ids_tuple in enumerate(rows, start=1):
    #        if num > 1:
    #            print("В выборке найдена дополнительная строка с номером: "+phone+"\n")
    #            print(sql+"\n")
    #        if not ids_tuple[0]:
    #            print("в выборке нет данных: "+phone+"\n")
    #            print(sql+"\n")
    #        if num < 1:
    #            print(" на всякий случай 141 стр:"+phone+"\n")
    #            print(sql+"\n")

    #        ids = str(ids_tuple[0])
    #        return ids

def insert_agregator(date):
    try:
        print(date)

        sql = "INSERT INTO agregator (number_advert, \
                                      advert_text, \
                                      status, \
                                      short_text_advert, \
                                      name_organisation, \
                                      long_text_advert, \
                                      advert_type, \
                                      createtion_date, \
                                      end_advert_date, \
                                      date_of_conclusion, \
                                      region, \
                                      url) \
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        connect = conn()
        cur = connect.cursor()
        with connect:
            cur.execute(sql, (date[0], date[2], date[1], date[4], date[3], date[5], date[6], date[7], date[8], date[9], date[10], date[11]))
        connect.close
    except Exception as e:
        print(e)
#############################################################################################################################################################
#
#
#############################################################################################################################################################
#
#
#############################################################################################################################################################
logic_work()


#    parse_date(source_index_page, link)
