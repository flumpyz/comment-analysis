# -*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

import os
import argparse
from urllib.parse import urlparse, parse_qs
from video_comments import VideoComment
import urllib
from urllib import request
import json
apiKey = "AIzaSyCBylxi4V37XA58B1JbhbUvMrvsbgSrHpg"

os.makedirs("bot/output", exist_ok=True)
parser = argparse.ArgumentParser()


def getCommentsFromVideo(videourl, maxComments):
    parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
    parser.add_argument("--max", help="number of comments to return", default=10)
    parser.add_argument("--videourl", help="Required URL for which comments to return", required=True)
    parser.add_argument("--key", help="Required API key", required=True)
    video_id = urlparse(str(videourl))
    q = parse_qs(video_id.query)
    vid = q["v"][0]

    vc = VideoComment(maxComments, vid, apiKey)
    vc.get_video_comments()


def get_information_from_youtube_video(video_id):
    base_info_url = 'https://www.googleapis.com/youtube/v3/videos?'

    info_url = base_info_url + 'part=statistics&key={}&id={}'.format(apiKey, video_id)

    print(info_url)
    inp = urllib.request.urlopen(info_url)
    resp = json.load(inp)

    return resp['items'][0]['statistics']['commentCount']