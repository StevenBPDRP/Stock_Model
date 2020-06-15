import pandas as pd
from datetime import datetime
import csv

with open('src/Source/Wind_SCode.txt', 'r', encoding='utf-8-sig') as ff:
    list_stock = ff.readlines()[0].split(',')


def select(path):
    """
    :return: list of candidates
    """
    data = pd.read_csv(path)
    p = path.replace('Wande_Data', 'Good')
    with open(p, 'w', newline='', encoding='utf-8-sig')as f:
        w = csv.writer(f)
        w.writerow([i for i in data])
        for i in range(len(data)):
            if 150 > data['PE_Mean'][i] > 0 and 0 < data['PE_Now/PE_Mean'][i] <= 0.9 and data['平均年化收益率'][i] > 0 \
                    and 4500000000 <= data['总市值'][i] <= 135000000000 and data['现金净流量_Now'][i] > 0:
                if data['ROE_Now'][i] != data['ROE_Now'][i] or data['ROE_Now'][i] > 8:
                    if data['机构预测涨幅空间'][i] > 130 or data['均值回归预测涨幅空间'][i] > 130:
                        w.writerow(data.loc[i])
    f.close()


def combine(path1, path2, path3):
    """
    :param path1: 3 years, must have a path!
    :param path2: 2 years
    :param path3: 1 years
    :return: list of good companies
    """
    d1 = pd.read_csv(path1)
    data1 = list(d1['股票代码'])
    d_stock = dict()
    d_po = dict()
    d_mr = dict()
    for i in range(len(data1)):
        d_stock[data1[i]] = d1['公司名称'][i]
        d_po[data1[i]] = d1['机构预测涨幅空间'][i]
        d_mr[data1[i]] = d1['均值回归预测涨幅空间'][i]

    try:
        data2 = list(pd.read_csv(path2)['股票代码'])
        if len(data2) == 0:
            data2 = list_stock
        else:
            pass
    except:
        data2 = list_stock

    try:
        data3 = list(pd.read_csv(path3)['股票代码'])
        if len(data3) == 0:
            data3 = list_stock
        else:
            pass
    except:
        data3 = list_stock

    good = set(data1).intersection(set(data2)).intersection(set(data3))
    good = list(good)
    good_c = [d_stock[i] for i in good]
    good_po = [d_po[i] for i in good]
    good_mr = [d_mr[i] for i in good]

    output = pd.DataFrame()
    output['股票代码'] = good
    output['公司名称'] = good_c
    output['机构预测涨幅空间'] = good_po
    output['均值回归预测涨幅空间'] = good_mr

    ylj = list(pd.read_excel('src/Data/养老金.xlsx')['股票代码'])
    cxg = list(pd.read_excel('src/Data/次新股.xlsx')['股票代码'])
    lylj = []
    lcxg = []

    for i in range(len(output)):
        if output['股票代码'][i] in ylj:
            lylj.append(1)
        else:
            lylj.append(0)

        if output['股票代码'][i] in cxg:
            lcxg.append(1)
        else:
            lcxg.append(0)

    output['有无养老金持仓'] = lylj
    output['是否次新股'] = lcxg

    output.to_excel('src/Stock_Data/Good_Stocks/优质股票' + datetime.now().strftime("%Y%m%d") + '.xlsx',
                    encoding='utf-8-sig', index=False)
    return output
