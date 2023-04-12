#!/usr/bin/env python3

import scrapetube
import random
import secrets
import subprocess
import sys

# Rambalac = UCAcsAE1tpLuP3y7UhxUoWpQ
# Moskas = UCy_OincP87AxXo4BFgjngDA
videos = scrapetube.get_channel("UCy_OincP87AxXo4BFgjngDA")
# video_list = []
video_id = []
# for video in videos:
#    # print(video["videoId"])
#    video_list.append(video)
for video in videos:
    video_id.append(video["videoId"])


# print(len(video_list))
# for vid in video_list:
#    print(
#        vid["title"]["runs"][0]["text"] + " https://youtube.com/watch/" + vid["videoId"]
#    )
random_video = str(
    "https://youtube.com/watch/" + video_id[random.randint(0, len(video_id) - 1)]
)
# random_id = video_id[(random.randint(0, len(video_id)))]
# print(random_id)
# print(video_list[random(0, len(video_list))]["videoId"])
# print(random_video)
subprocess.run(["mpv", random_video])
