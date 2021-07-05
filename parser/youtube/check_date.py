import csv
import re
from datetime import datetime


def check_date():
    hashmap = {}
    with open('list_to_csv.csv', newline='') as csv_file:
        cr = csv.reader(csv_file, delimiter=',')
        for row in cr:
            line = row[0]
            arr = line.split(',')
            url = arr[0].replace('\'', '')
            url = url.replace('[', '')
            date = arr[len(arr)-1]
            hashmap[url] = (datetime.strptime(date[2:12], "%Y-%m-%d"))
    print(hashmap)
    return hashmap



