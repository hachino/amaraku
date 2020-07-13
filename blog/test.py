# coding: UTF-8
import csv
import os
import datetime
import locale
import random

# Create your views here.
rank_csv_paths = [
    "/Users/akira_mac/python_work/amaraku/data/cosme/cosme.csv",
    "/Users/akira_mac/python_work/amaraku/data/pet/pet.csv",
    "/Users/akira_mac/python_work/amaraku/data/kaden/kaden.csv",
]

random_item_list = []

for i in rank_csv_paths:
    with open(i, newline="") as data :
        reader = csv.reader(data)
        for row in reader:
            if row[12] == "1":
                random_item_list.append(row)

print(random.choices(random_item_list,k=10))