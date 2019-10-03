from selenium.webdriver import Chrome
import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
# 換頁訊息隱藏在api裡面，手動製作一個變更網址url執行換頁動作
# url = 'https://rent.591.com.tw/?kind=0&region=1&firstRow=30&totalRows=11401'
# 第一頁url
# url = 'https://rent.591.com.tw/?kind=0&region=1'

c = ["房屋名稱", "出租者","出租者身份","地址","租金","坪數","樓層","型態","現況","聯絡電話","押金","車位","最短租期","寵物","身份要求","性別要求","開伙"]
df = pd.DataFrame(columns=c)

count=0
for i in range(0,8106+30,30):
    driver = Chrome("./chromedriver")
    driver.get('https://rent.591.com.tw/?kind=0&region=1&firstRow='+str(i))
    time.sleep(3)
    driver.find_element_by_xpath("/html/body/div[5]/div[1]/div[2]/dl[1]/dd[2]").click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,"html.parser")

    soup.find("div",class_="pull-left hasData")
    time.sleep(1)
    # href=" //rent.591.com.tw/rent-detail-8143810.html "
    a=soup.find('div',class_="listLeft").find_all('a',{'href': re.compile('tw/rent-detail-*')})

    classweb=[]
    for i in a:
         if str(i['href']) not in classweb:
            classweb.append(i['href'].replace(' ',''))
    classuni = list(set(classweb))
    print(classuni)
    for web in classuni:
        url = 'https:'+str(web)
        print(url)
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
            }
        r = requests.get(url,headers=head)
        r.encoding='utf8'
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            price = soup.find('div',class_="price").text.replace('\n','').replace(' ','').replace(",","").split('元')[0]
            title = soup.find('span',class_="houseInfoTitle").text
            addr = soup.find('span',class_="addr").text
            renter_all = soup.find('div',class_="avatarRight").text.replace(' ','').replace('\n','')
            renter=""
            identify=""
            if "(仲介，" in renter_all:
                renter=renter_all[:3]
                identify =re.split('\(|\)',renter_all)[1]
            else:
                renter = re.split('（',renter_all)[0].replace(' ',"")
                identify = re.split('（|）',renter_all)[1]
            #上欄位
            ulattr = soup.find('ul',class_="attr").find_all('li')
            size=""
            floor=""
            housetype=""
            situation=""
            for attr in ulattr :
                attr = attr.text
                if "坪數" in attr:
                    size = attr.split(':')[1].replace(' ','').replace("坪","")
                elif "樓層" in attr:
                    floor = re.split(':|/',attr)[1].replace(' ','').replace("F","")
                elif "型態" in attr:
                    housetype = attr.split(':')[1].replace(' ','')
                elif "現況" in attr:
                    situation = attr.split(':')[1].replace(' ','')
            phone = soup.find_all('span',class_="dialPhoneNum")
            for num in phone:
                phonenum = str(num).split('"')[3]

            #下欄位
            labellist = soup.find('ul',class_="clearfix labelList labelList-1").find_all('li')
            deposit=""
            car=""
            short_rent=""
            cook=""
            chara=""
            sex=""
            pet=""

            for label in labellist:
                label = label.text
                if "押金" in label:
                    deposit = label.split('：')[1].replace(' ','')
                elif "車 位" in label:
                    car = label.split('：')[1].replace(' ','')
                elif "最短租期" in label:
                    short_rent = label.split('：')[1].replace(' ','')
                elif "寵物" in label:
                    pet = label.split('：')[1].replace(' ','')
                elif "身份要求" in label:
                    chara = label.split('：')[1].replace(' ','')
                elif "性別要求" in label:
                    sex = label.split('：')[1].replace(' ','')
                elif "開伙" in label:
                    cook = label.split('：')[1].replace(' ','')
            print("房屋名稱:",title)
            print('出租者:',renter)
            print('出租者身份:',identify)
            print("地址:",addr)
            print("租金:",price)
            print("坪數:",size)
            print("樓層:",floor)
            print("型態:",housetype)
            print("現況:",situation)
            print("聯絡電話:",phonenum)
            print("押金:",deposit)
            print("車位:",car)
            print("最短租期",short_rent)
            print("寵物:",pet)
            print("身份要求:",chara)
            print("性別要求:",sex)
            print("開伙:",cook)
            count+=1
            print('第 %s 筆:' % count )
            print('--------------------------------------------------')
            xxx = pd.Series([title,renter,identify,addr,price,size,floor,housetype,situation,phonenum,deposit,
                            car,short_rent,pet,chara,sex,cook],index=c)
            df = df.append(xxx, ignore_index=True)
        except:
            continue
    print(count)

df.to_csv("591_newtapei_houses.csv", encoding="utf-8", index=False)