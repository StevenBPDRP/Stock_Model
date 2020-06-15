from selenium import webdriver
import time
import csv
import pandas as pd


def YLJ_list():
    """
    :return: list of yanglaojin
    """
    driver = webdriver.Chrome(executable_path='src/Source/chromedriver.exe')
    driver.get('http://data.jrj.com.cn/gudong/yljcg.shtml')
    time.sleep(1)
    data = driver.find_element_by_xpath('//*[@id="table-1"]').text

    for i in range(3):
        time.sleep(0.5)
        d = driver.find_element_by_xpath('//*[@id="table-1"]').text
        d = d.replace('排名 股票代码 股票名称\n公告日期\n养老金账户名 持股数(万股) 占总股本比例 占流通股本比例 最新收盘价 涨跌幅','')
        data += d
        driver.find_element_by_xpath('//*[@id="pagebar1"]/a[5]').click()

    driver.close()

    return data


def YLJ_csv(data):
    """
    :param data: data of YLJ_list
    :return: csv
    """
    data = data.replace('\n', ' ')
    data = data.split(' ')
    with open('Data/Source/养老金.csv', 'w', newline='', encoding='utf-8-sig')as f:
        w = csv.writer(f)
        w.writerow(data[:10])
        for i in range(int(len(data) / 10)):
            w.writerow(data[10 + i * 10:20 + i * 10])
    f.close()
    x = pd.read_csv('src/Source/养老金.csv', dtype={1: str})
    l = list(x['股票代码'])
    for i in range(len(x)):
        if l[i][:2] == '00' or l[i][:2] == '30':
            l[i] += '.SZ'
        else:
            l[i] += '.SH'
    x['股票代码'] = l
    x = x[['股票代码', '股票名称', '公告日期', '养老金账户名', '持股数(万股)', '占总股本比例', '占流通股本比例']]
    x = x.drop_duplicates()
    x.to_excel('src/Source/养老金.xlsx', encoding='utf-8-sig', index=False)
