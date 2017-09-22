#coding=utf-8
import urllib
import re
import time
import MySQLdb

cityURLAddr = ["http://www.pm25.com/beijing.html",\
        "http://www.pm25.com/shanghai.html",\
        "http://www.pm25.com/guangzhou.html",\
        "http://www.pm25.com/shenzhen.html",\
        "http://www.pm25.com/hangzhou.html",\
        "http://www.pm25.com/chengdu.html",\
        "http://www.pm25.com/nanjing.html",\
        "http://www.pm25.com/wuhan.html",\
        "http://www.pm25.com/xian.html",\
        "http://www.pm25.com/tianjin.html",\
        "http://www.pm25.com/xiaogan.html"]

cityNameArray = ["chengdu", "wuhan", "shenzhen","hangzhou","beijing"]
rankURLAddr = "http://www.pm25/rank"

#获取网页数据
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

#提取城市AQI数据
def getAQI4City(cityURLAddr):
    html = getHtml(cityURLAddr)
    reg = 'mon="选择监测点".*aqi=.[0-9]*'
    regGetNum = '\d+$'
    cityAQI = re.findall(reg,html)
    cityAQIInfo = re.findall(regGetNum,cityAQI[0])
    return cityAQIInfo[0]

#提取城市排名数据
def getCityRankNum(cityURLAddr):
    html = getHtml(cityURLAddr)
    cityRankInfo = re.findall(r'目前城市排名 [0-9]*' , html)
    if (cityRankInfo):
        cityRankNum = re.findall(r'\d+$',cityRankInfo[0])
        return cityRankNum[0]
    else:
        return 0


#写入数据库
def insertData2DataBase(cityName,AQI,RankNum,Time):
    tableName = "weather_data"
    cur = conn.cursor()
    sqli="insert into %s values('%s',%s,%s,'%s')" % (tableName, cityName, AQI, RankNum, str(Time))
    cur.execute(sqli)
    cur.close()
    conn.commit()


#开始执行
x=1
conn = MySQLdb.connect(host = 'localhost',port = 3306,user = 'root',passwd = '111111',db = 'weather')
while x<2:
    for i in range(0,11,1):
        cityName = re.findall('[a-z]+',cityURLAddr[i])
        AQI = getAQI4City(cityURLAddr[i])
        RankNum = getCityRankNum(cityURLAddr[i])
        currentTime = time.strftime("%Y%m%d_%H:%M:%S", time.localtime())
        insertData2DataBase(cityName[4],int(AQI),int(RankNum),currentTime)
        format = '%-*s AQI: %-*s Rank: %-*s Current Time: %s'
        print format % (10, cityName[4],4,AQI, 4,RankNum, currentTime)
        
    x = x+1
    #time.sleep(3600)
    print '\n'
conn.close()
