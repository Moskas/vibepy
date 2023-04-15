#!/usr/bin/env python3
import os
import random
import argparse
import subprocess
import scrapetube


CACHE_DIR = os.path.join(
    os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "vibepy"
)


def play_video(video_id):
    subprocess.run(["mpv", f"https://youtube.com/watch?v={video_id}"])


def get_unique_random_video(video_ids, previous_video_id=None):
    video_id = None
    while not video_id or video_id == previous_video_id:
        video_id = random.choice(video_ids)
    return video_id


def get_video_ids(channel_id=None, playlist_id=None, update_cache=False):
    if channel_id:
        cache_file = os.path.join(CACHE_DIR, f"{channel_id}.txt")
        if os.path.exists(cache_file) and not update_cache:
            with open(cache_file, "r") as f:
                return [line.strip() for line in f.readlines()]
        else:
            videos = scrapetube.get_channel(channel_id)
    elif playlist_id:
        cache_file = os.path.join(CACHE_DIR, f"{playlist_id}.txt")
        if os.path.exists(cache_file) and not update_cache:
            with open(cache_file, "r") as f:
                return [line.strip() for line in f.readlines()]
        else:
            videos = scrapetube.get_playlist(playlist_id)
    else:
        return None

    video_ids = [video["videoId"] for video in videos]
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_file, "w") as f:
        f.write("\n".join(video_ids))

    return video_ids


def main():
    parser = argparse.ArgumentParser(
        description="A script to play random youtube video from a given channel/playlist"
    )
    parser.add_argument(
        "-i", "--channel-id", action="store", help="ID of the YouTube channel"
    )
    parser.add_argument(
        "-p", "--playlist-id", action="store", help="ID of the YouTube playlist"
    )
    parser.add_argument(
        "-c",
        "--continuous",
        action="store_true",
        help="If argument is present activates continuous playback mode",
    )
    parser.add_argument(
        "-u",
        "--update-cache",
        action="store_true",
        help="Update the cache file with latest video IDs",
    )
    args = parser.parse_args()

    if not args.channel_id and not args.playlist_id:
        print("No channel/playlist id provided")
        exit()

    video_ids = get_video_ids(args.channel_id, args.playlist_id, args.update_cache)

    if not video_ids:
        print("Failed to get video IDs")
        exit()

    if args.continuous:
        previous_video_id = None
        while True:
            print("Playing in a continuous mode")
            video_id = get_unique_random_video(video_ids, previous_video_id)
            play_video(video_id)
            previous_video_id = video_id
    else:
        video_id = get_unique_random_video(video_ids)
        play_video(video_id)


if __name__ == "__main__":
    main()
