from urllib import request
import urllib
import json
import csv
import check_date as cd
from database_for_videos_scripts import DataBaserForVideos


def write_comments_from_channel_to_database(channel_id):
    api_key = "AIzaSyCadW9QMKGKC6KV9eO0qu1ZavQwvjnch_E"

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key,
                                                                                                        channel_id)

    video_links = []
    url = first_url
    while True:
        inp = request.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            if i['id']['kind'] == "youtube#video":
                video_links.append([base_video_url + i['id']['videoId'],
                                    i['id']['videoId'],
                                    i['snippet']['title'],
                                    i['snippet']['publishTime']])

        try:
            next_page_token = resp['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)
        except:
            break

    DataBaserForVideos.insert_channel_to_database(channel_id)
    return check_download_dates_and_write_to_database(video_links, channel_id)

    # Коммент Наташи 09.07:
    # video_links - список списков, который содержит списки, в каждом из которых:
    # [0] - ссылка на видео, [1] - id видео, [2] - название видео, [3] - дата публикации видео
    # написать метод, который сверит дату ([3]) и в зависимости от неё положит в базу данных (табличка videos) видео,
    # то есть ссылку, название, дату, id должен назначаться автоматически, там стоит автоинкремент
    # метод в идеале должен возвращать массив id всех видео, которые мы сложили в бд, чтобы я могла через запросы к бд
    # достать все комменты и построить диаграмму
    # Также парсер переписать, чтобы он не в файл складывал комментарии, а в бд, и также туда записывал дату
    # загрузки и название
    #

    # закомментила, чтобы не в файл складывать ссылки, а в бд
    # with open("list_to_csv.csv", 'w', newline='', encoding='utf-8') as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     for item in video_links:
    #         csv_writer.writerow([item])


# Проверяет даты всех видео, те, которые подходят - складывает в бд и возвращает список id видео, которые подошли
def check_download_dates_and_write_to_database(video_links, channel_id):
    video_id_list = []
    for video in video_links:
        if cd.check_date_of_download(video[3]):
            video_id = video[1]
            video_name = video[2]
            video_link = video[0]
            download_date = video[3]
            video_id_list.append(
                DataBaserForVideos.insert_video_to_database(video_id, video_name, video_link, download_date, channel_id))
    return video_id_list



