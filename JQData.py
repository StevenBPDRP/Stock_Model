from jqdatasdk import *
import numpy as np
from datetime import datetime
import pandas as pd

with open(r'src\Source\JQ_SCode.txt', 'r', encoding='utf-8-sig')as ff:
    daima = eval(ff.readlines()[0])


def Concept_list(security):
    """
    :param security: code of security
    :return: concept list of this security
    """
    con = get_concept(normalize_code(security), datetime.now().strftime("%Y-%m-%d"))
    output = list()
    for i in con[normalize_code(security)]['jq_concept']:
        output.append(i['concept_name'])
    return output


def Industry_name(security):
    """
    :param security: code of security
    :return: industry of this security
    """
    ind = get_industry(normalize_code(security), date=None)
    try:
        return ind[normalize_code(security)]['jq_l2']['industry_name'].replace('指数', '')
    except:
        try:
            return ind[normalize_code(security)]['jq_l1']['industry_name'].replace('指数', '')
        except:
            return '其他'


def Price_csv(security):
    """
    :param security: code of security
    :return: csv of its price in 3 years
    """
    return get_price(normalize_code(security), start_date=datetime.now().strftime("%Y-%m-%d").replace('2020', '2017'),
                     end_date=datetime.now().strftime("%Y-%m-%d"), frequency='daily', fields=None, skip_paused=False,
                     fq='pre', count=None, panel=True, fill_paused=True)


def Price_analyse(security):
    """
    :param security: code of security
    :return: beta, safe buying price
    """
    sz_matrix = pd.read_csv(r'Data\Source\000001.csv', encoding='gbk')
    sz_return = sz_matrix['涨跌幅']

    p_matrix = Price_csv(security)
    close = np.array(p_matrix['close'])

    # 1个月，3个月，半年，1年的股价30%低位线
    safe1 = np.percentile(close[-30:], 30)
    safe3 = np.percentile(close[-90:], 30)
    safe6 = np.percentile(close[-180:], 30)
    safe12 = np.percentile(close[-365:], 30)

    # 3个月、1年的beta值
    s_return = np.diff(close) * 100 / close[:-1]
    beta3 = np.cov(s_return[-90:], np.array([float(i) for i in sz_return[:90][::-1]]))
    beta3 = beta3[0][1] / beta3[1][1]
    beta12 = np.cov(s_return[-365:], np.array([float(i) for i in sz_return[:365][::-1]]))
    beta12 = beta12[0][1] / beta12[1][1]

    # 3个月、1年的alpha值
    alpha3 = np.mean(s_return[-90:]) - np.mean([float(i) for i in sz_return[:90][::-1]])
    alpha12 = np.mean(s_return[-365:]) - np.mean([float(i) for i in sz_return[:365][::-1]])
    return [safe1, safe3, safe6, safe12, round(alpha3, 2), round(alpha12, 2), round(beta3, 2), round(beta12, 2)]


def main_f(path_goods):
    """
    :param path_goods: path of good_stock.csv
    :return: csv + safe1, safe3, safe6, safe12, alpha3, alpha12, beta3, beta12, industry_name
    """
    l_security = pd.read_excel(path_goods)
    safe1 = []
    safe3 = []
    safe6 = []
    safe12 = []
    alpha3 = []
    alpha12 = []
    beta3 = []
    beta12 = []
    i_n = []

    for i in list(l_security['股票代码']):
        l = Price_analyse(i)
        i_n.append(Industry_name(i))
        safe1.append(l[0])
        safe3.append(l[1])
        safe6.append(l[2])
        safe12.append(l[3])
        alpha3.append(l[4])
        alpha12.append(l[5])
        beta3.append(l[6])
        beta12.append(l[7])

    l_security['所属板块'] = i_n
    l_security['安全买入价格_1M'] = safe1
    l_security['安全买入价格_3M'] = safe3
    l_security['安全买入价格_6M'] = safe6
    l_security['安全买入价格_12M'] = safe12

    l_security['beta_3M'] = beta3
    l_security['beta_12M'] = beta12

    l_security['alpha_3M'] = alpha3
    l_security['alpha_12M'] = alpha12

    l_security.to_excel('src/Stock_Data/Good_Stocks/优质股票' + datetime.now().strftime("%Y%m%d") + '.xlsx')
