import json
from pathlib import Path

import pandas as pd
from turftopic import KeyNMF

data = pd.read_csv("DATA/csv_files/yidali-huarenjie_19-05-2025-recent.csv")
data = data[data["text"].isna()==False]
corpus = list(data["text"])

with Path("DATA/keywords/yidali-huarenjie_19-05-2025-recent_gen_keywords10.jsonl").open() as in_file:
    keywords = []
    for line in in_file:
        line = line.strip()
        if line:
            keywords.append(json.loads(line))


#len(keywords) == len(corpus)

## NO NEED TO SPECIFY EMBEDDING MODEL WHEN YOU HAVE THE KEYWORDS
model = KeyNMF(n_components=10)
doc_topic_matrix = model.fit_transform(corpus, keywords=keywords)

for topic_name, topic_strength in zip(model.topic_names, doc_topic_matrix.T):
    data[topic_name] = topic_strength

data.to_excel("outputs/yidali-huarenjie-phase3/10_topics/yidali-huarenjie_10topics_distributions.xlsx", index=False, header=True)
