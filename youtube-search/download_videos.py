from numpy import row_stack
from pytube import Playlist
import ssl
import re
import pickle 

ssl._create_default_https_context = ssl._create_stdlib_context
YOUTUBE_STREAM_AUDIO = '140' # modify the value to download a different stream
DOWNLOAD_DIR = '/Users/sunnydasgupta/code/ask-nk/youtube-search/mp3'

playlist = Playlist('https://www.youtube.com/watch?v=-CgXDjsV8Tc&list=UULFF2v8v8te3_u4xhIQ8tGy1g')

# this fixes the empty playlist.videos list
playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

print(len(playlist.video_urls))

videos_dict = {}

for url in playlist.video_urls:
# physically downloading the audio track
    for video in playlist.videos:
        try: 
            video.title
        except:
            title = "Title not found"
            print("Something went wrong when writing to the file")
        else: 
            title = video.title
        # create entry in dict
        videos_dict[video.video_id] = {
            'title': title,
            'url': f"{url}"
        }
        print (videos_dict)
        with open('videos_dict.pkl', 'wb') as f:
            f.truncate(0)
            pickle.dump(videos_dict, f)
        try: 
            video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
        except:
            print("Something went wrong when streaming audio")
        else: 
            stream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
        audioStream = stream
        audioStream.download(output_path=DOWNLOAD_DIR, filename=f"{video.video_id}.mp3")


with open('videos_dict.pkl', 'wb') as f:
    pickle.dump(videos_dict, f)

