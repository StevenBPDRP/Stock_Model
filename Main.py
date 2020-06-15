import Wind
import MeanReversion
import SZ
import JQData
from datetime import datetime

if __name__ == '__main__':
    SZ.sz()

    a = Wind.data_to_csv_wande(Wind.data_gether_wande(90), 3)
    b = Wind.data_to_csv_wande(Wind.data_gether_wande(30), 1)
    c = Wind.data_to_csv_wande(Wind.data_gether_wande(60), 2)

    try:
        d = MeanReversion.select(
            'Data/Stock_Data/Wande_Data_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
        e = MeanReversion.select(
            'Data/Stock_Data/Wande_Data_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
        f = MeanReversion.select(
            'Data/Stock_Data/Wande_Data_' + str(2) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
    except:
        d = MeanReversion.select(
            'Data/Stock_Data/Wande_Data_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
        e = MeanReversion.select(
            'Data/Stock_Data/Wande_Data_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')

    try:
        g = MeanReversion.combine('Data/Stock_Data/Good_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv',
                                  'Data/Stock_Data/Good_' + str(2) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv',
                                  'Data/Stock_Data/Good_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
    except:
        g = MeanReversion.combine('Data/Stock_Data/Good_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv',
                                  '',
                                  'Data/Stock_Data/Good_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')

    JQData.main_f('Data/Stock_Data/Good_Stocks/优质股票' + datetime.now().strftime("%Y%m%d") + '.xlsx')