import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from datetime import timedelta
import re
import csv
import pandas as pd
import time
datelist=[]
def get_new_url(day):
    mae='http://www1.mbrace.or.jp/od2/K/'
    ato='.html'
    return requests.get(mae+day+ato)
def isHarfKana(value):
    return re.match(r"^[ｦ-ﾟ]+$", value) is not None
def isFull(value):
    return re.match(r"^[^\x01-\x7E]+$", value) is not None
def isHarf(value):
    return re.match(r"^[\x20-\x7E]+$", value) is not None
strdt=dt.strptime('20190101','%Y%m%d')
enddt=dt.strptime('20200630','%Y%m%d')
days_num=(enddt-strdt).days+1
for j in range(days_num):
    datelist.append(strdt+timedelta(days=j))
data_colmuns=['track','weather','wind_direction','wind_power','wave',
'1st','motor1','boat1','entry1','2nd','motor2','boat2','entry2',
'3rd','motor3','boat3','entry3','4th','motor4','boat4','entry4',
'5th','motor5','boat5','entry5','6th','motor6','boat6','entry6',
'tan1','fuku_1','fuku_2','tan2','fuku2','tan3','fuku3']
index=[]
load=12



boat_race_track=['kiryu','toda','edogawa','heiwajima','tamagawa','hamanako',
'gamagori','tokoname','tsu','mikuni','biwako','suminoe','amasaki','naruto',
'marugame','kojima','miyajima','tokuyama','shimonoseki','wakamatsu','ashiya','fukuoka','karatsu','omura']


for s in range(1,25):
    track=boat_race_track[s-1]
    if s<10:site='0'+str(s)
    else :site=str(s)
    for d in datelist:
        day=d.strftime('%Y%m/'+site+'/%d')
        res=get_new_url(day)
        content_type_encoding = res.encoding if res.encoding != 'ISO-8859-1' else None
        soup=bs(res.content,'html.parser',from_encoding=content_type_encoding)
        #処理をかく
        
        if  soup.find('title')==None:#取得できる場合
            data_all=soup.find_all('pre')
            del data_all[0]
            for pre_data in data_all:
                er_fg=False
                data=str(pre_data).split()
                include_data=[]
                this_race=[[],[],[],[],[],[]]
                basis=data.index('--------------------------------------------------------------------')
                weather=data[basis-21]
                wind_direction=data[basis-19]
                wind_power=data[basis-18].strip('m波')
                wave=data[basis-17].strip('cm')
                basis+=3
                for k in range(6):
                    if data[basis-2]!='0'+str(k+1):
                        er_fg=True
                        break
                    this_race[k].append(data[basis])
                    basis+=1
                    while isFull(data[basis]):
                        basis+=1
                    this_race[k].append(data[basis])
                    this_race[k].append(data[basis+1])
                    this_race[k].append(data[basis+3])
                    basis+=8
                    if data[basis-3]=='.':
                        basis+=1
                try:    
                    tan1=data[basis]
                    fuku_1=data[basis+3]
                    fuku_2=data[basis+5]
                    tan2=data[basis+8]
                    fuku2=data[basis+13]
                    tan3=data[basis+31]
                    fuku3=data[basis+36]
                    include_data+=[track,weather,wind_direction,wind_power,wave]
                    for i in this_race:
                        for j in i:
                            include_data.append(j)
                    include_data+=[tan1,fuku_1,fuku_2,tan2,fuku2,tan3,fuku3]
                except:
                    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$   error on '+str(day)+'at '+track)
                if er_fg==False:
                    index.append(include_data)
                else:
                    print('warning on '+str(day))
        print('loading...'+str(load)+' at '+site)
        load+=12
        time.sleep(0.7)
        

df=pd.DataFrame(data=index,columns=data_colmuns)
df.to_csv('race_data.csv',index=False,encoding='utf-8')

#処理をかく
