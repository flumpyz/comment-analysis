# -*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

from collections import defaultdict
import json
import pandas as pd
from helper import openURL
from config import YOUTUBE_COMMENT_URL
from database_for_videos_scripts import DataBaserForVideos


class VideoComment:
    def __init__(self, max_results, video_id, key):
        self.comments = defaultdict(list)
        self.replies = defaultdict(list)
        self.params = {
            'part': 'snippet,replies',
            'maxResults': max_results,
            'videoId': video_id,
            'textFormat': 'plainText',
            'key': key
        }

    def load_comments(self, mat):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            self.comments["id"].append(comment["id"])
            self.comments["comment"].append(comment["snippet"]["textDisplay"])
            self.comments["author"].append(comment["snippet"]["authorDisplayName"])
            self.comments["likecount"].append(comment["snippet"]["likeCount"])
            self.comments["publishedAt"].append(comment["snippet"]["publishedAt"])

            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    self.replies["parentId"].append(reply["snippet"]["parentId"])
                    self.replies["authorDisplayName"].append(reply['snippet']['authorDisplayName'])
                    self.replies["replyComment"].append(reply["snippet"]["textDisplay"])
                    self.replies["publishedAt"].append(reply["snippet"]["publishedAt"])
                    self.replies["likeCount"].append(reply["snippet"]["likeCount"])

    def get_video_comments(self):
        url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        self.load_comments(url_response)

        while nextPageToken:
            self.params.update({'pageToken': nextPageToken})
            url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
            nextPageToken = url_response.get("nextPageToken")
            self.load_comments(url_response)
        self.write_comments_to_database()
        # self.create_df()

    # Сделать так, чтобы данные из словарей клались в бд, а не в файл
    def create_df(self):
        df = pd.DataFrame().from_dict(self.comments)
        df.to_csv("parent_video_comment.csv")

        df = pd.DataFrame().from_dict(self.replies)
        df.to_csv("comment_reply.csv")

    def write_comments_to_database(self):
        DataBaserForVideos.insert_comments_to_database(self.comments["comment"], self.params["videoId"])
        DataBaserForVideos.insert_comments_to_database(self.replies["comment"], self.params["videoId"])
