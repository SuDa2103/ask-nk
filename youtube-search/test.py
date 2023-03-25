from pytube import Playlist
import ssl
import re
ssl._create_default_https_context = ssl._create_stdlib_context

YOUTUBE_STREAM_AUDIO = '140' # modify the value to download a different stream
DOWNLOAD_DIR = '/Users/sunnydasgupta/code/ask-nk/youtube-search'

playlist = Playlist('https://www.youtube.com/watch?v=-CgXDjsV8Tc&list=UULFF2v8v8te3_u4xhIQ8tGy1g')

# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

print(len(playlist.video_urls))

for url in playlist.video_urls:
    print(url)

# physically downloading the audio track
for video in playlist.videos:
    audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
    audioStream.download(output_path=DOWNLOAD_DIR)

