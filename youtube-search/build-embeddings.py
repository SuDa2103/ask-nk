from datasets import load_dataset  # !pip install datasets

data = load_dataset(
    "jamescalam/youtube-transcriptions",
    split="train",
  	revision="8dca835"
)
data

data[0]

data[1]


data[2]

from tqdm.auto import tqdm

new_data = []

window = 6  # number of sentences to combine
stride = 3  # number of sentences to 'stride' over, used to create overlap

for i in tqdm(range(0, len(data), stride)):
    i_end = min(len(data)-1, i+window)
    if data[i]['title'] != data[i_end]['title']:
        # in this case we skip this entry as we have start/end of two videos
        continue
    text = ' '.join(data[i:i_end]['text'])
    new_data.append({
        'start': data[i]['start'],
        'end': data[i_end]['end'],
        'title': data[i]['title'],
        'text': text,
        'id': data[i]['id'],
        'url': data[i]['url'],
        'published': data[i]['published']
    })


new_data[0]

new_data[100]

new_data[500]

from sentence_transformers import SentenceTransformer

model_id = "multi-qa-mpnet-base-dot-v1"

model = SentenceTransformer(model_id)
model

dim = model.get_sentence_embedding_dimension()

import pinecone

index_id = "youtube-search"

pinecone.init(
    api_key="f112f55d-c1a3-42e9-8618-24d3277dd23b",  # app.pinecone.io
    environment="us-west4-gcp"
)

if index_id not in pinecone.list_indexes():
    pinecone.create_index(
        index_id,
        dim,
        metric="dotproduct"
    )

index = pinecone.Index(index_id)
index.describe_index_stats()

from tqdm.auto import tqdm

# we encode and insert in batches of 64
batch_size = 64

# loop through in batches of 64
for i in tqdm(range(0, len(new_data), batch_size)):
    # find end position of batch (for when we hit end of data)
    i_end = min(len(new_data)-1, i+batch_size)
    # extract the metadata like text, start/end positions, etc
    batch_meta = [{
        "text": new_data[x]["text"],
        "start": new_data[x]["start"],
        "end": new_data[x]["end"],
        "url": new_data[x]["url"],
        "title": new_data[x]["title"]
    } for x in range(i, i_end)]
    # extract only text to be encoded by embedding model
    batch_text = [row['text'] for row in new_data[i:i_end]]
    # create the embedding vectors
    batch_embeds = model.encode(batch_text).tolist()
    # extract IDs to be attached to each embedding and metadata
    batch_ids = [row['id'] for row in new_data[i:i_end]]
    # 'upsert' (eg insert) IDs, embeddings, and metadata to index
    to_upsert = list(zip(batch_ids, batch_embeds, batch_meta))
    index.upsert(to_upsert)

index.describe_index_stats()

query = "what is OpenAI's CLIP?"

xq = model.encode(query).tolist()

index.query(xq, top_k=5, include_metadata=True)