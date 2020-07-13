# coding: UTF-8
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from mysite.settings import BASE_DIR
import csv
import os
import datetime
import locale
import random

# Create your views here.
def about(request):
    return render(request, 'blog/about.html')

def rank_top(request):

    rank_csv_paths = [
        BASE_DIR + "/data/cosme/cosme.csv",
        BASE_DIR + "/data/pet/pet.csv",
        BASE_DIR + "/data/kaden/kaden.csv",
    ]

    random_item_list = []

    for i in rank_csv_paths:
        with open(i, newline="") as data :
            reader = csv.reader(data)
            for row in reader:
                if row[12] == "1":
                    random_item_list.append(row)

    random_otoku_items = random.choices(random_item_list,k=10)

    return render(request, 'blog/rank_top.html',{'otoku_items':random_otoku_items})

def rank_shop(request, pk, shop):
    
    CSV_PATH = BASE_DIR + "/data/" + shop + "/" + shop + ".csv"
    ITEM_LIST = []

    shopdict = {
        'cosme': 'コスメ',
        'pet': 'ペット',
        'kaden': 'パソコン/周辺機器',

    }

    shopname = shopdict[shop]

    filetime = os.path.getmtime(CSV_PATH)
    dt = datetime.datetime.fromtimestamp(filetime)
    gettime = dt.strftime('%Y/%m/%d %H:%M')

    with open(CSV_PATH, newline="") as data :
        reader = csv.reader(data)
        for row in reader:
            ITEM_LIST.append(row)

    start = (pk-1) * 100
    end = pk * 100

    for i, item in enumerate(ITEM_LIST):
        if int(item[4]) > start:
            begin = i
            break

    for i, item in enumerate(ITEM_LIST):
        if int(item[4]) > end:
            last = i
            break
        last = i

    ITEM_LIST = ITEM_LIST[begin:last]

    # weekday = datetime.date.today().weekday()
    # if weekday == 1 or weekday == 4 :
    #     wpoint = 2

    today = datetime.date.today()
    getday = today.strftime('%d')
    if "0" in getday or "5" in getday:
        gotopoint = 2
    else:
        gotopoint = 0

    return render(request, 'blog/rank_shop.html', {'itemlist':ITEM_LIST, 'shop':shop, 'gettime':gettime, 'shopname':shopname, "gotopoint":gotopoint})