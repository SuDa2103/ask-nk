import whisper
import torch  # pytorch install steps: pytorch.org
from pathlib import Path
from tqdm.auto import tqdm
import json
from download_videos import videos_dict

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

model = whisper.load_model("medium.en").to(device)

# get list of MP3 audio files
paths = [str(x) for x in Path('./mp3').glob('*.mp3')]
print(len(paths))
print(paths[:5])

# we get the IDs like so
paths[0].split('/')[-1][:-4]

data = []
for i, path in enumerate(tqdm(paths)):
    _id = path.split('/')[-1][:-4]
    # transcribe to get speech-to-text data
    result = model.transcribe(path)
    # add results to data list
    data.extend(result['segments'])

# set window (length of text chunk) and stride
window = 1
stride = 1  # smaller stride creates overlap

data = []

results = []
with open("transcription.jsonl", "w", encoding="utf-8") as fp:
    for i, path in enumerate(tqdm(paths)):
        _id = path.split('/')[-1][:-4]
        # transcribe to get speech-to-text data
        result = model.transcribe(path)
        segments = result['segments']
        # get the video metadata...
        video_meta = videos_dict[_id]
        for j in range(0, len(segments), stride):
            j_end = min(j+window, len(segments)-1)
            text = ''.join([x["text"] for x in segments[j:j_end]])
            start = segments[j]['start']
            end = segments[j_end]['end']
            row_id = f"{_id}-t{segments[j]['start']}"
            meta = {
                **video_meta,
                **{
                    "id": row_id,
                    "text": text.strip(),
                    "start": start,
                    "end": end
                }
            }
            data.append(meta)
            json.dump(meta, fp)
            fp.write('\n')

len(data)

existing_ids = []

with open("transcription.jsonl", 'r', encoding='utf-8') as fp:
    for line in fp:
        obj = json.loads(line)
        existing_ids.append(obj['url'].split('/')[-1])

existing_ids = set(existing_ids)
len(existing_ids)

list(existing_ids)[:5]

paths = [str(x) for x in Path('./mp3').glob('*.mp3')]
print(len(paths))
print(paths[:5])

paths = [x for x in paths if x.split('/')[-1][:-4] not in existing_ids]
print(len(paths))
print(paths[:5])

# set window (length of text chunk) and stride
window = 1
stride = 1  # smaller stride creates overlap

results = []
with open("transcription.jsonl", "a", encoding="utf-8") as fp:
    for i, path in enumerate(tqdm(paths)):
        _id = path.split('/')[-1][:-4]
        # transcribe to get speech-to-text data
        result = model.transcribe(path)
        segments = result['segments']
        # get the video metadata...
        video_meta = videos_dict[_id]
        for j in range(0, len(segments), stride):
            j_end = min(j+window, len(segments)-1)
            text = ''.join([x["text"] for x in segments[j:j_end]])
            start = segments[j]['start']
            end = segments[j_end]['end']
            _id = f"{_id}-t{segments[j]['start']}"
            meta = {
                **video_meta,
                **{
                    "id": _id,
                    "text": text.strip(),
                    "start": start,
                    "end": end
                }
            }
            json.dump(meta, fp)
            fp.write('\n')

len(data)