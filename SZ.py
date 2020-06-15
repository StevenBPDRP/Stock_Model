from selenium import webdriver
import time
import os
import shutil

def sz():
    driver = webdriver.Chrome(executable_path=r'Data\Source\chromedriver.exe')
    driver.get('http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html')

    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="downloadData"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="dropBox1"]/div[2]/form/div[3]/a[1]').click()

    time.sleep(3)
    driver.close()
    try:
        os.remove('Data/Source/000001.csv')
    except:
        pass
    shutil.move(r'C:\Users\xxx\Downloads\000001.csv','src/Source/000001.csv')



