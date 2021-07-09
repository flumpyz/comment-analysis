import csv
import re
import time
from datetime import datetime
import videoParser
import commentParser as cp


class Date_Checker:

    @staticmethod
    def get_key(dic, value):
        for k, v in dic.items():
            if v == value:
                return k

    @staticmethod
    def check_date(start, end):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        hashmap = {}
        with open('list_to_csv.csv', newline='', encoding='utf-8') as csv_file:
            cr = csv.reader(csv_file, delimiter=',')
            for row in cr:
                line = row[0]
                arr = line.split(',')
                url = arr[0].replace('\'', '')
                url = url.replace('[', '')
                if len(arr) == 4:
                    date = arr[3]
                elif len(arr) == 5:
                    date = arr[4]
                hashmap[url] = (datetime.strptime(date[2:12], "%Y-%m-%d"))
        hash_date = hashmap.values()
        fileclean = open('channel_comment.txt', 'w', encoding='utf-8')
        fileclean.close()
        for item in hash_date:
            if start_date <= item <= end_date:
                url = Date_Checker.get_key(hashmap, item)
                print(url)
                cp.getCommentsFromVideo(url, 0)
                with open('parent_video_comment.csv', 'r', encoding='utf-8') as a_file:
                    a_content = a_file.read()
                with open('channel_comment.txt', 'a', encoding='utf-8')as b_file:
                    b_file.write(a_content)
            else:
                continue





