from selenium import webdriver
import time
import csv
import pandas as pd


def CXG_list():
    """
    :return: csv of cxg
    """
    driver = webdriver.Chrome(executable_path='Data/Source/chromedriver.exe')
    driver.get('https://q.stock.sohu.com/cn/bk_2011.shtml')

    time.sleep(1)
    tab = driver.find_element_by_xpath('//*[@id="BIZ_MS_plstock"]').text
    driver.close()

    return tab


def CXG_csv(data):
    """
    :param data: data of str, data = CXG_list()
    :return: csv
    """
    data = data.replace(' ', '\n')
    data = data.replace('点击按代码排序查询\n', '')
    data = data.split('\n')
    with open('Data/Source/次新股.csv', 'w', newline='', encoding='utf-8-sig')as f:
        w = csv.writer(f)
        w.writerow(data[:12])
        for i in range(int(len(data) / 12)):
            w.writerow(data[12 + 12 * i:24 + 12 * i])
    f.close()
    lstock = pd.read_csv('Data/Source/次新股.csv',dtype={0:str})
    s_indx = [str(i) for i in lstock['股票代码']]
    for j in range(len(lstock)):
        if s_indx[j][:2]=='00' or s_indx[j][:2]=='30':
            s_indx[j]+='.SZ'
        else:
            s_indx[j]+='.SH'
    lstock['股票代码'] = s_indx
    lstock = lstock[['股票代码','股票名称']]
    lstock.to_excel('Data/Source/次新股.xlsx',index=False,encoding='utf-8-sig')

