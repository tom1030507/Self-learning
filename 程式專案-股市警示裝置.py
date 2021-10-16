import twstock
import requests
import datetime
import json
import time
from threading import Timer
import pandas as pd
def stock_history(stock_list):
    for i in range(len(stock_list)):
        mk = twstock.codes[i]
        if mk.market == "上市":            
            tse_list.append(i)
        elif mk.market == "上櫃":
            otc_list.append(i)
        stock = twstock.Stock(i)
        price = stock.price[-20:]
        ma5 = sum(price[-4:])/4
        ma10 = sum(price[-9:])/9
        ma20 = sum(price[-19:])/19
        ma.loc[i] = [ma5,ma10,ma20]
        time.sleep(1)
def stock_crawler():
    stock_list = '|'.join('tse_{}.tw'.format(tse) for tse in tse_list) + '|' + '|'.join('otc_{}.tw'.format(otc) for otc in otc_list) 
    url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + stock_list
    data = json.loads(requests.get(url).text)
    data = data['msgArray']
    for i in range(len(data)):
        pz = data[i]['z']
        print(pz)
        if (ma.loc[i]['5ma']>=pz):
            print(data[i]['c'],data[i]['n']," 跌破五日線 限價:",pz," 5ma=",ma.loc[i]['5ma']," 10ma=",ma.loc[i]['10ma']," 20ma=",ma.loc[i]['20ma'])
        elif (ma.loc[i]['10ma']>=pz):
            print(data[i]['c'],data[i]['n']," 跌破十日線 限價:",pz," 5ma=",ma.loc[i]['5ma']," 10ma=",ma.loc[i]['10ma']," 20ma=",ma.loc[i]['20ma'])
        elif (ma.loc[i]['20ma']>=pz):
            print(data[i]['c'],data[i]['n']," 跌破月線 限價:",pz," 5ma=",ma.loc[i]['5ma']," 10ma=",ma.loc[i]['10ma']," 20ma=",ma.loc[i]['20ma'])
    Timer(1,stock_crawler).start()
    time = datetime.datetime.now() 
    start_time = datetime.datetime.strptime(str(time.date())+'9:30', '%Y-%m-%d%H:%M')
    end_time =  datetime.datetime.strptime(str(time.date())+'13:30', '%Y-%m-%d%H:%M')
    if (time<=start_time and time>=end_time):
        Timer(1,stock_crawler).cancel()
        print("收盤結束程式")
print("正在載入中...請稍後")
ma = pd.read_csv('ma.csv',header=0,index_col=0)
tse_list = []
otc_list = []
if (len(list(ma.index))!=0):
    stock_history(list(ma.index))
Timer(1,stock_crawler).start()
print("載入成功")
print("詳見指令,請輸入help")
while True:
    try: 
        command = input().split(" ")
        if (len(command)==1):
            if (command[0]=="quit"):
                ma.to_csv('ma.csv') 
                break
            elif (command[0]=="help"):
                print("指令:")
                print("help : 查找指令")
                print("quit : 結束程式")
                print("list : 查找自選單中股票")
                print("add + 股票代碼 : 增加股票代碼到自選單中")
                print("del + 股票代碼 : 從自選單中刪除股票代碼")
            elif (command[0]=="list"):
                if (len(list(ma.index))==0):
                    print("尚未加入任何股票")
                else:
                    print("此選單為以下:")
                    for i in list(ma.index):
                        print(i)
            else: 
                print("輸入錯誤,輸入help查找指令")
        elif (len(command)==2):
            if (command[0]=="add"):
                try:
                    stock_history(command[1])
                    print("添加成功")
                except:
                    print("此代碼不存在")    
            elif (command[0]=="del"):
                if (command[1] in list(ma.index)):
                    ma = ma.drop([command[1]])
                    print("刪除成功")
                else:
                    print('此代碼沒在清單中')
            else:
                print("輸入錯誤,輸入help查找指令")
    except:
        print("輸入錯誤,輸入help查找指令")