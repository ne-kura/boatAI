# -*- coding: utf-8 -*-
import csv
import pandas as pd
import re

data_columns=['id','name','rank','sex',
'age','height','weight','win_rate','double_win_rate','start_timing_ave',
'course1_win','course2_win','course3_win','course4_win','course5_win',
'last_rank','last_rank2','last_ability','ability']
index=[]

def isHarfKana(value):
    return re.match(r"^[ｦ-ﾟ]+$", value) is not None
def isFull(value):
    return re.match(r"^[^\x01-\x7E]+$", value) is not None
def isHarf(value):
    return re.match(r"^[\x20-\x7E]+$", value) is not None

data_file=open("racer_data.txt","rt")
for data in data_file:
    this_line_data=[]
    scope=0
    #id追加
    ida=data[scope:4]
    scope+=4
    #name追加
    name=''
    while not isHarfKana(data[scope]):
        if data[scope].find('　')==-1:
            if isFull(data[scope]):
                name+=data[scope]
        scope+=1
    #rank追加
    while isHarfKana(data[scope]) or isHarf(data[scope]):
        scope+=1
    scope+=2
    rank=data[scope:scope+2]
    #sex追加
    scope+=9
    if data[scope]=='1':
        sex="M"
    else:
        sex='F'
    scope+=1
    #age追加
    age=(data[scope:scope+2])
    scope+=2
    #height
    height=(data[scope:scope+3])
    scope+=3
    #weight
    weight=(data[scope:scope+2])
    scope+=5
    #win_rate
    win_rate=data[scope]
    win_rate+='.'
    win_rate+=(data[scope+1:scope+3])
    scope+=4
    #double_win_rate
    double_win_rate=data[scope:scope+2]
    double_win_rate+='.'
    double_win_rate+=data[scope+2]
    scope+=16
    #start_timing_ave
    start_timing_ave=data[scope:scope+3]
    scope+=7
    #course1_win
    course1_win=data[scope:scope+2]+'.'+data[scope+2]
    scope+=13
    #course2_win
    course2_win=data[scope:scope+2]+'.'+data[scope+2]
    scope+=13
    #course3_win
    course3_win=data[scope:scope+2]+'.'+data[scope+2]
    scope+=13
    #course4_win
    course4_win=data[scope:scope+2]+'.'+data[scope+2]
    scope+=13
    #course5_win
    course5_win=data[scope:scope+2]+'.'+data[scope+2]
    scope+=22
    #last_rank
    last_rank=data[scope:scope+2]
    scope+=2
    #last_rank2
    last_rank2=data[scope:scope+2]
    scope+=4
    #last_ability
    last_ability=data[scope:scope+4]
    #ability
    ability=data[scope:scope+4]
    
    this_line_data+=[ida,name,rank,sex,age,height,weight,win_rate,double_win_rate,start_timing_ave,course1_win,course2_win,course3_win,course4_win,course5_win,last_rank,last_rank2,last_ability,ability]
    index.append(this_line_data)
data_file.close()
df=pd.DataFrame(data=index,columns=data_columns)
print(df)
df.to_csv('racer_data.csv',index=False,encoding='utf-8')

