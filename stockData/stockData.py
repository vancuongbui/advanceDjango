

import requests #pip install requests
from bs4 import BeautifulSoup   #pip install bs4
import csv
from datetime import datetime
import parse    #pip install parse
from selenium import webdriver  #pip install selenium, then copy chromedriver.exe to the same folder
import time



#the following is the URL of FPT stock price information from cafef.vn
driver = webdriver.Chrome()
URL = ("http://banggia2.ssi.com.vn")
driver.get(URL)   #get the html page in raw content
#print(html_page)
#lable the stock information in a list of name
StockFields = ['ThoiGian', 'Tran','San','TC','KL3','Gia3','KL2','Gia2','KL1','Gia1','Gia','KL','thayDoi','Gia1','KL1','Gia2','KL2','Gia3','KL3','Cao','Thap','TB','TongKL','GiaP1','KLP1','GiaP2','KLP2','NNMua','NNBan','Room']
StockDataList = []
StockDataList.append(StockFields)


def getStockPrice(sticker):
    #driver.refresh()
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #file = open('ssiIndex.txt','w+', encoding='utf-8')
    #file.write(soup.prettify())

    tr_target = 'tr' + str(sticker)
    stock_table_row = soup.find('tr', {'id':tr_target})  #locate table data of sticker
    
    tdtag = stock_table_row.find_all('td', {'class':'cell'})  #locate the table data for FPT
    receivedTime = datetime.now().strftime("%H:%M:%S")
    stockData = [receivedTime]
    for i in range(0, len(tdtag)):
        stockData.append(tdtag[i].text)
    
    return stockData

def main():
    file = open('FPTPrice.txt','a+', encoding='utf-8')
    file.writelines("%8s\t" % field for field in StockFields)
    file.write('\n')
    for j in range(0,100):
        FPTStocEntry = getStockPrice('FPT')
        #StockDataList.append(FPTStocEntry)
        #file = open('FPTPrice.txt','a+', encoding='utf-8')
        file.writelines("%8s\t" % item for item in FPTStocEntry)   
        file.write('\n')
    file.close()
    
main()

   



