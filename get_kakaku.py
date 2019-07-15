#!/usr/local/bin/python3

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def convert_list(data):
    html = BeautifulSoup(data, 'lxml')
    table = html.find_all('table', attrs={'class': 'alignC tblBorderGray02 mTop5'})[0]
    records = table.find_all('tr', class_=False)
    pr_list = []
    for record in records:
        record_dict = {}
        try:
            record_dict['id'] = record.select('input[type=checkbox]')[0].attrs['value']
            record_dict['price'] = record.find('span', class_='priceText').find('a').text
            record_dict['storage'] = record.find('label', attrs={'title': 'ストレージ容量'}).text
        except:
            break

        pr_list.append(record_dict)

    return pr_list

# ノートPCスペック検索
url = 'http://kakaku.com/specsearch/0020/'
product_list = []
driver = webdriver.Safari()
driver.get(url)

# 価格情報のあるモデルだけ
driver.find_element_by_id('lDispNonPrice').click()
while True:
    data = driver.page_source
    product_list = product_list + convert_list(data)
    try:
        driver.find_element_by_class_name('paging').find_elements_by_tag_name('a')[-1].find_element_by_tag_name('span').click()
    except:
        break
    time.sleep(4)

df = pd.DataFrame(product_list)
df.to_csv("notepc.csv")
