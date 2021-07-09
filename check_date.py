import csv
from datetime import datetime
import commentParser
import copy_cSv

begin_period = datetime(2020, 9, 22, 0, 0)
end_period = datetime(2021, 7, 1, 0, 0)


def get_key(dic, value):
    for k, v in dic.items():
        if v == value:
            return k


def check_date_of_download(date_of_download):
    return begin_period <= datetime.strptime(date_of_download, "%Y-%m-%dT%H:%M:%SZ") <= end_period
    # Закомментила, не нужно
    # hashmap = {}
    # with open('list_to_csv.csv', newline='', encoding='utf-8') as csv_file:
    #     cr = csv.reader(csv_file, delimiter=',')
    #     for row in cr:
    #         line = row[0]
    #         arr = line.split(',')
    #         url = arr[0].replace('\'', '')
    #         url = url.replace('[', '')
    #         date = arr[len(arr) - 1]
    #         hashmap[url] = (datetime.strptime(date[2:12], "%Y-%m-%d"))
    # hash_date = hashmap.values()
    # return hashmap

    # file_clean = open('newtest.csv', "w+")
    # file_clean.close()
    # return check_date_phase_two(hash_date, hashmap)

# Наташа: написала метод, который сверяет даты и возвращает словарь ссылок на видео и дат, которые подходят по дате
# Но он бесполезен будет, когда перепишем videoParser
def get_dictionary_of_video_links_with_correct_date_and_date():
    hashmap = check_date_of_download()
    dictionary_of_link_key_and_value_date = {}
    for key in hashmap:
        if begin_period <= hashmap[key] <= end_period:
            dictionary_of_link_key_and_value_date[key] = hashmap[key]
        else:
            continue
    return dictionary_of_link_key_and_value_date


def check_date_phase_two(hash_date, hashmap):
    for el in hash_date:
        if begin_period <= el <= end_period:
            commentParser.get_comments_from_video(get_key(hashmap, el), 0)
            return copy_cSv.copy_please()
        elif el < begin_period or el > end_period:
            continue
        else:
            return print("That's all")
