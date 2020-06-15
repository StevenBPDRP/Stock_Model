from selenium import webdriver
import pandas as pd
import time
from WindPy import w
from datetime import datetime
from datetime import timedelta


def data_collect_jsl():
    """
    :return: 高pe及roe数据
    """
    driver = webdriver.Chrome(executable_path='src/Source/chromedriver.exe')
    driver.get('https://www.jisilu.cn/data/stock/dividend_rate/#cn')
    time.sleep(0.5)

    # 高roe
    roe = driver.find_element_by_xpath('//*[@id="flex_cn"]/thead/tr[2]/th[15]')
    roe.click()
    time.sleep(0.1)
    roe.click()
    data_roe = driver.find_element_by_xpath('//*[@id="flex_cn"]/tbody').text
    # 高pe
    pe = driver.find_element_by_xpath('//*[@id="flex_cn"]/thead/tr[2]/th[8]')
    pe.click()
    data_pe = driver.find_element_by_xpath('//*[@id="flex_cn"]/tbody').text

    return data_roe, data_pe


def data_alltogether_wande():
    """
    :return: 所有股票roe，pe情况
    """
    index = ['总市值', 'PE', 'PE预测', '年化收益率_100weeks', '年化收益率_2years', '预测净利润', 'ROE', '预测ROE', '评级', '预测目标价格',
             '收盘价', '成交量']
    w.start()

    with open('Data/Source/wande.txt', 'r')as f:
        l = f.readlines()
    while '\n' in l:
        l.remove('\n')
    for i in l:
        i = i.replace('\n', '')
        i = i.replace('2020-04-19', datetime.now().strftime("%Y-%m-%d"))
        x = eval(i).Data
        y = pd.DataFrame()
        for j in range(len(index)):
            y[index[j]] = x[j + 2]
        y.to_csv('Data/Stock_Data/' + x[0][0] + '.csv', index=False, encoding='utf-8-sig')
    w.stop()


def data_gether_wande(dates):
    """
    :param dates: 周期
    :return: 12个周期内，股票基本面情况
    """
    w.start()
    with open('src/Source/wande.txt', 'r') as f:
        l = f.readlines()[0]
    l = l.replace('20200503', datetime.now().strftime("%Y%m%d"))
    x = eval(l).Data
    for i in range(1, 13):
        l = l.replace((datetime.now() + timedelta(days=-(i - 1) * dates)).strftime("%Y%m%d"),
                      (datetime.now() + timedelta(days=-i * 90)).strftime("%Y%m%d"))
        l = l.replace('comp_name,industry_citic,ev,', '')
        y = eval(l).Data
        x += y
    return x


def data_to_csv_wande(x, years):
    """
    :param x: data_gether_wande(dates)
    :param years: 1 or 2 or 3
    :return: all stock data
    """
    index = ['公司名称', '行业', '总市值',
             'PE_Now', '年化收益率_100weeks_Now', 'ROE_Now', '净利润_Now', '每股营业收入_Now', '现金净流量_Now', '预测目标价格_Now', '收盘价_Now',
             'PE_1', '年化收益率_1', 'ROE_1', '净利润_1', '每股营业收入_1', '现金净流量_1', '预测目标价格_1', '收盘价_1',
             'PE_2', '年化收益率_2', 'ROE_2', '净利润_2', '每股营业收入_2', '现金净流量_2', '预测目标价格_2', '收盘价_2',
             'PE_3', '年化收益率_3', 'ROE_3', '净利润_3', '每股营业收入_3', '现金净流量_3', '预测目标价格_3', '收盘价_3',
             'PE_4', '年化收益率_4', 'ROE_4', '净利润_4', '每股营业收入_4', '现金净流量_4', '预测目标价格_4', '收盘价_4',
             'PE_5', '年化收益率_5', 'ROE_5', '净利润_5', '每股营业收入_5', '现金净流量_5', '预测目标价格_5', '收盘价_5',
             'PE_6', '年化收益率_6', 'ROE_6', '净利润_6', '每股营业收入_6', '现金净流量_6', '预测目标价格_6', '收盘价_6',
             'PE_7', '年化收益率_7', 'ROE_7', '净利润_7', '每股营业收入_7', '现金净流量_7', '预测目标价格_7', '收盘价_7',
             'PE_8', '年化收益率_8', 'ROE_8', '净利润_8', '每股营业收入_8', '现金净流量_8', '预测目标价格_8', '收盘价_8',
             'PE_9', '年化收益率_9', 'ROE_9', '净利润_9', '每股营业收入_9', '现金净流量_9', '预测目标价格_9', '收盘价_9',
             'PE_10', '年化收益率_10', 'ROE_10', '净利润_10', '每股营业收入_10', '现金净流量_10', '预测目标价格_10', '收盘价_10',
             'PE_11', '年化收益率_11', 'ROE_11', '净利润_11', '每股营业收入_11', '现金净流量_11', '预测目标价格_11', '收盘价_11',
             'PE_12', '年化收益率_12', 'ROE_12', '净利润_12', '每股营业收入_12', '现金净流量_12', '预测目标价格_12', '收盘价_12']

    y = pd.DataFrame()
    with open(r'src\Source\Wind_SCode.txt', 'r', encoding='utf-8-sig')as ff:
        daima = ff.readlines()[0]

    y['股票代码'] = daima.split(',')
    for a in range(len(index)):
        try:
            y[index[a]] = x[a]
        except:
            return x

    y['机构预测涨幅空间'] = [round(y['预测目标价格_Now'][i] / y['收盘价_Now'][i] * 100, 2) for i in range(len(y))]
    penow = list(y['PE_Now'])
    if penow != [-999] * len(y):
        y['PE_Mean'] = [(y['PE_12'][i] + y['PE_11'][i] + y['PE_10'][i] + y['PE_9'][i] + y['PE_8'][i] + y['PE_7'][i] +
                         y['PE_6'][i] + y['PE_5'][i] +
                         y['PE_4'][i] + y['PE_3'][i] + y['PE_2'][i] + y['PE_1'][i] + y['PE_Now'][i]) / 13 for i in
                        range(len(y))]
        y['PE_Now/PE_Mean'] = [y['PE_Now'][i] / y['PE_Mean'][i] for i in range(len(y))]
    else:
        y['PE_Mean'] = [(y['PE_12'][i] + y['PE_11'][i] + y['PE_10'][i] + y['PE_9'][i] + y['PE_8'][i] + y['PE_7'][i] +
                         y['PE_6'][i] + y['PE_5'][i] + y['PE_4'][i] + y['PE_3'][i] + y['PE_2'][i] + y['PE_1'][i]) / 12
                        for i in
                        range(len(y))]
        y['PE_Now/PE_Mean'] = [y['PE_1'][i] / y['PE_Mean'][i] for i in range(len(y))]

    y['平均年化收益率'] = [(y['年化收益率_12'][i] + y['年化收益率_11'][i] + y['年化收益率_10'][i] + y['年化收益率_9'][i] + y['年化收益率_8'][i] +
                     y['年化收益率_7'][i] + y['年化收益率_6'][i] + y['年化收益率_5'][i] + y['年化收益率_4'][i] + y['年化收益率_3'][i] +
                     y['年化收益率_2'][i] + y['年化收益率_1'][i] + y['年化收益率_100weeks_Now'][i]) / 13 for i in range(len(y))]

    y['ROE_Mean'] = [(y['ROE_12'][i] + y['ROE_11'][i] + y['ROE_10'][i] + y['ROE_9'][i] + y['ROE_8'][i] + y['ROE_7'][i] +
                      y['ROE_6'][i] + y['ROE_5'][i] + y['ROE_4'][i] + y['ROE_3'][i] + y['ROE_2'][i] + y['ROE_1'][i] +
                      y['ROE_Now'][i]) / 13 for i in range(len(y))]

    y['ROE_Now/ROE_Mean'] = [y['ROE_Now'][i] / y['ROE_Mean'][i] for i in range(len(y))]
    y['均值回归预测价格'] = [y['收盘价_Now'][i] / y['PE_Now/PE_Mean'][i] for i in range(len(y))]
    y['均值回归预测涨幅空间'] = [round(y['均值回归预测价格'][i] / y['收盘价_Now'][i]*100,2) for i in range(len(y))]
    y['机构预测目标价格_Now'] = y['预测目标价格_Now']

    new_index = ['股票代码', '公司名称', '行业', '总市值',
                 'PE_12', 'PE_11', 'PE_10', 'PE_9', 'PE_8', 'PE_7', 'PE_6', 'PE_5', 'PE_4', 'PE_3', 'PE_2', 'PE_1',
                 'PE_Now', 'PE_Mean', 'PE_Now/PE_Mean',
                 '年化收益率_12', '年化收益率_11', '年化收益率_10', '年化收益率_9', '年化收益率_8', '年化收益率_7', '年化收益率_6',
                 '年化收益率_5', '年化收益率_4', '年化收益率_3', '年化收益率_2', '年化收益率_1', '年化收益率_100weeks_Now', '平均年化收益率',
                 'ROE_12', 'ROE_11', 'ROE_10', 'ROE_9', 'ROE_8', 'ROE_7', 'ROE_6', 'ROE_5', 'ROE_4', 'ROE_3', 'ROE_2',
                 'ROE_1', 'ROE_Now',
                 'ROE_Mean', 'ROE_Now/ROE_Mean',
                 '净利润_12', '净利润_11', '净利润_10', '净利润_9', '净利润_8', '净利润_7', '净利润_6', '净利润_5', '净利润_4', '净利润_3', '净利润_2',
                 '净利润_1', '净利润_Now',
                 '每股营业收入_12', '每股营业收入_11', '每股营业收入_10', '每股营业收入_9', '每股营业收入_8', '每股营业收入_7', '每股营业收入_6',
                 '每股营业收入_5', '每股营业收入_4', '每股营业收入_3', '每股营业收入_2', '每股营业收入_1', '每股营业收入_Now',
                 '现金净流量_12', '现金净流量_11', '现金净流量_10', '现金净流量_9', '现金净流量_8', '现金净流量_7', '现金净流量_6', '现金净流量_5',
                 '现金净流量_4', '现金净流量_3', '现金净流量_2', '现金净流量_1', '现金净流量_Now',
                 '收盘价_Now',
                 '均值回归预测价格','机构预测目标价格_Now','均值回归预测涨幅空间', '机构预测涨幅空间']
    y = y[new_index]
    y.to_csv('src/Stock_Data/Wande_Data_' + str(years) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv', index=False,
             encoding='utf-8-sig')
    return y
