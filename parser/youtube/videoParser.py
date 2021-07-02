import urllib.request
import json
import csv

def getVideoFromChannel(channel_id):
    api_key = "AIzaSyD1OpkSMxv3y2v93rY5WJ5GpW4hIZ1QiZo"

    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key,
                                                                                                        channel_id)

    video_links = []
    url = first_url
    while True:
        inp = urllib.request.urlopen(url)
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
    return video_links

    with open(SAVE_PATH+"search_channel_id.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for item in video_links:
            csv_writer.writerow([item])