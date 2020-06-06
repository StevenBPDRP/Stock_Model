import Data_Collect
import MeanReversion
from datetime import datetime

if __name__ == '__main__':
    a = Data_Collect.data_to_csv_wande(Data_Collect.data_gether_wande(90), 3)
    b = Data_Collect.data_to_csv_wande(Data_Collect.data_gether_wande(30), 1)
    c = Data_Collect.data_to_csv_wande(Data_Collect.data_gether_wande(60), 2)

    d = MeanReversion.select('Data/Wande_Data_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
    e = MeanReversion.select('Data/Wande_Data_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
    f = MeanReversion.select('Data/Wande_Data_' + str(2) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
    try:
        g = MeanReversion.combine('Data/Good_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv',
                                  'Data/Good_' + str(2) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv',
                                  'Data/Good_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
    except:
        g = MeanReversion.combine('Data/Good_' + str(3) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv',
                                  '', 'Data/Good_' + str(1) + 'Y_' + datetime.now().strftime("%Y%m%d") + '.csv')
