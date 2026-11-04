from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
from sentence_transformers import SentenceTransformer
from turftopic import KeyNMF
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.special import softmax
from datetime import datetime
from gensim.models.coherencemodel import CoherenceModel
from gensim.models import Nmf
import pandas as pd
import numpy as np
import random
import jieba
import umap
import json
from pathlib import Path

''' Get saved keywords for given source from saved jsonl files '''
def stream_keywords(s):
    with open("../DATA/keywords/" + s + "_keywords.jsonl") as keyword_file:
        for line in keyword_file:
            yield json.loads(line.strip())

''' Tokenize texts using jieba '''
def tokenize_zh(text):
    words = jieba.lcut(text)
    return words

def clean(obj):
    if isinstance(obj, dict):
        return {clean(k): clean(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [clean(i) for i in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

date = "19-05-2025" # UPDATE WITH NEW DATA
num_topics = 10 # UPDATE WITH RELEVANT # OF TOPICS

sites = [#"xinouzhou_" + date + "_gen",
        "oushinet_" + date + "_gen"]#,
         #"chinanews_" + date + "_gen"]
         #"yidali-huarenjie_" + date + "_gen",
         #"ihuawen_" + date + "_gen"]

# Load stop words from https://github.com/stopwords-iso/stopwords-zh/blob/master/stopwords-zh.txt
with open("../DATA/stopwords-zh.txt") as file:
    stopwords = file.readlines()
stopwords = [s.strip() for s in stopwords]

# Loop through and create topic models for each source
embeddings = []
texts = []
times = []
for s in sites:
    print(s)

    # Load embeddings and texts
    embeddings = np.load("../DATA/embeddings/" + s + ".npy")
    csv_file = pd.read_csv("../DATA/csv_files/" + s.replace("_gen", "") + ".csv")

    # Filter to only articles with text
    has_text = np.nonzero(~csv_file["text"].isna())
    csv_file = csv_file.loc[has_text]
    embeddings = embeddings[has_text]

    # Create lists of texts and times for dynamic modeling
    texts = csv_file["text"].tolist()
    times = csv_file["datetime"].tolist()
    times = [t if t != "2024-05-07_12-19" else "2024-05-07_12-15" for t in times]
    times = [datetime.strptime(d.replace("_", " "),"%Y-%m-%d %H-%M") for d in times]

    # Find unique timestamps
    unique_times = list(set(times))
    unique_times.sort()
    unique_times.append(datetime.strptime("2025-05-19 15-18", "%Y-%m-%d %H-%M"))

    # Load componenets
    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2",
                                          device="mps")

    vectorizer = CountVectorizer(tokenizer=tokenize_zh,
                                 stop_words = stopwords)

    model = KeyNMF(encoder = embedding_model,
                   vectorizer=vectorizer,
                   n_components=num_topics)

    print("Extracting keywords...")
    # Save keywords for source
    with open("../DATA/keywords/" + s + "_keywords10.jsonl", "w") as file:
        keywords = model.extract_keywords(texts)
        for k in keywords:
            clean_k = {key: float(val) for key, val in k.items()}
            file.write(json.dumps(clean(k)) + "\n")

    # Load saved keywords
    #with Path("../DATA/keywords/" + s + "_keywords10.jsonl").open() as in_file:
    #    keywords = []
    #    for line in in_file:
    #        line = line.strip()
    #        if line:
    #            keywords.append(json.loads(line))
    #print(keywords)

    # Fit topic model
    print("Fitting model...")
    doc_top_matrix = model.fit_transform_dynamic(texts,
                                                 timestamps=times,
                                                 bins=unique_times,
                                                 embeddings=embeddings,
                                                 keywords=keywords)

    # Save plotted topics over time
    print("Saving results...")
    model.plot_topics_over_time().write_html("../DATA/figures/" + s + "_time_series_" + str(num_topics) + ".html")

    # Save topics over time
    topics_over_time = model.get_topics_over_time()
    out_file = open("../DATA/topic_terms/" + s + "_" + str(num_topics) + ".json", "w")
    clean_topics = clean(topics_over_time)
    json.dump(clean_topics, out_file)

    # Save topic importances
    temporal_topic_importance = model.temporal_importance_
    with open('../DATA/topic_matrices/' + s + '_' + str(num_topics) + '.npy', 'wb') as f:
        np.save(f, temporal_topic_importance)
