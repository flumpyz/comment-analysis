import videoParser as cm
import check_date as cd
from datetime import datetime
import commentParser as cp
#import youtube.check_date as cd

#URLvid = "https://www.youtube.com/watch?v=vYkD3GU-rvA"
# cm.getVideoFromChannel('UCyEjQOeF0Vi6JC8zf5RCoHA')
import urllib.request
import json
import urllib
import pprint

cp.getCommentsFromVideo("https://www.youtube.com/watch?v=d5rvy5XPyzk", 200)
cm.write_comments_from_channel_to_database("UCyEjQOeF0Vi6JC8zf5RCoHA")

#change to yours VideoID or change url inparams
# cm.write_video_information_to_database(0)
# VideoID = "SZj6rAYkYOg"
#
# params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % VideoID}
# url = "https://www.youtube.com/oembed"
# query_string = urllib.parse.urlencode(params)
# url = url + "?" + query_string
#
# with urllib.request.urlopen(url) as response:
#     response_text = response.read()
#     data = json.loads(response_text.decode())
#     pprint.pprint(data)
#     print(data['title'])
#cd.check_date()

