# coding: UTF-8
import requests
import re
import csv
from bs4 import BeautifulSoup as bs4
import json
from time import sleep
import time
import datetime
import csv
import random
from ast import literal_eval
import mwsapi as ama

#定数
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:68.0) Gecko/20100101 Firefox/68.0"}
RAKUTEN_API_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628'
RAKUTEN_API_ID = "1098720660993966148"
RAKUTEN_API_AFFIID =  "1a215d3c.4afdeb08.1a215d3d.9d6adc29"

def asin_list_maker(asin_list_path, genreid):

    with open(asin_list_path) as f:
        s = f.read()
        itemdict = literal_eval(s)

    for i in range(10):

    # 100026 kaden
    # 100939 cosme
    # 101213 pet

        payload = {
            "genreId" : genreid,
            "page" : i+1,
            "applicationId" : RAKUTEN_API_ID,
            "period" : "realtime"
        }

        raku_api_res = requests.get(RAKUTEN_API_URL, params=payload)
        raku_api_json = raku_api_res.json()
        item_data_list = raku_api_json['Items']

        for i in range(29):
            try:
                item = item_data_list[i]["Item"]
                itemcode = item['itemCode']
                itemurl = item['itemUrl']
            except:
                continue

            if itemcode in itemdict:
                print("exist!")
                continue

            item_res = requests.get(itemurl,headers=HEADERS)
            item_res_parser = bs4(item_res.content, "html.parser")

            # JAN,shpcode,itemcodeを取得する処理               
            rancode = item_res_parser.find(id="ratRanCode")
            try:
                JAN = rancode["value"]
            except:
                continue
            itemdict[itemcode] = JAN
            time.sleep(1)
            print(JAN)

        with open(asin_list_path, "w", newline="") as f:
            print(itemdict, file=f)

def price_compare(asin_list_path, item_csv_path, today_data_path, genreid):

    today = datetime.date.today()

    with open(today_data_path) as f:
        s = f.read()
        today_data = literal_eval(s)

    if str(today) != today_data['today']:
        with open(today_data_path, "w", newline="") as f:
            print("""{'today':'""" + str(today) + """'}""" , file=f)

        with open(today_data_path) as f:
            s = f.read()
            today_data = literal_eval(s)

    with open(asin_list_path) as f:
        s = f.read()
        itemdict = literal_eval(s)

    # 100026 kaden
    # 100939 cosme
    # 101213 pet

    write_item_list = []

    for i in range(10):
        payload = {
            "genreId" : genreid,
            "page" : i+1,
            "affiliateId" : "1a215d3c.4afdeb08.1a215d3d.9d6adc29",
            "applicationId" : "1098720660993966148",
            "period" : "realtime"
        }

        print(i + 1)

        raku_api_res = requests.get(RAKUTEN_API_URL, params=payload)
        raku_api_json = raku_api_res.json()
        item_data_list = raku_api_json['Items']

        for s in range(29):
            try:
                item = item_data_list[s]["Item"]
                itemcode = item['itemCode']
                rakrank = item['rank']
                itemname = item['itemName']
                itemname = itemname[:40] + "•••"
                affiurl = item['itemUrl']
                shopname = item['shopName']
                itemprice = item['itemPrice']
                imageurl = item['mediumImageUrls'][0]['imageUrl']
                jan = itemdict[itemcode]
            except:
                continue

            print(rakrank)
            
            if itemcode in today_data:
                print("exist!")
                today_data[itemcode][4] = rakrank
                write_item_list.append(today_data[itemcode])
                continue

            if jan:
                try:
                    data = ama.asin_search(jan)
                    data2 = ama.product_search(data,float(itemprice))
                    asin = data2[0]
                    ama_price = str(data2[1])
                    ama_price = ama_price.replace(".0","")
                    ama_seller = data2[2]
                    category = data2[3]
                    amarank = data2[4]
                    fee_price = ama.fee_search(asin,ama_price)
                    fee_price = fee_price.replace(".00","")
                    if int(itemprice) < int(ama_price):
                        otoku_flag = 1
                    else:
                        otoku_flag = 0

                except:
                    data = ""
                    data2 = ""
                    asin = ""
                    ama_price = ""
                    ama_seller = ""
                    category = ""
                    amarank = ""
                    fee_price = ""
                    otoku_flag = 0
            else:
                data = ""
                data2 = ""
                asin = ""
                ama_price = ""
                ama_seller = ""
                category = ""
                amarank = ""
                fee_price = ""
                otoku_flag = 0

            item_list = [
                itemname,
                affiurl,
                shopname,
                itemprice,
                rakrank,
                imageurl,
                asin,
                ama_price,
                fee_price,
                ama_seller,
                category,
                amarank,
                otoku_flag,
            ]

            write_item_list.append(item_list)
            today_data[itemcode] = item_list
            
        now = datetime.datetime.now()
        today_data['get_time'] = now.strftime('%Y/%m/%d %H:%M')
            
    # if i == 0:
    with open(item_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        for item in write_item_list:
            try:
                writer.writerow(item)
                write_item_list = []
            except:
                writer.writerow("")
                item_list = []
    # else:
    #     with open(item_csv_path, "a", newline="") as f:
    #         writer = csv.writer(f)
    #         for item in write_item_list:
    #             try:
    #                 writer.writerow(item)
    #                 write_item_list = []
    #             except:
    #                 writer.writerow("")
    #                 item_list = []    

    with open(today_data_path, "w", newline="") as f:
        print(today_data, file=f)
