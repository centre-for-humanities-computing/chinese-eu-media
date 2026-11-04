import json
import pandas as pd
import numpy as np
from datetime import datetime
from itertools import chain

''' Get the terms from topic term list '''
def get_terms(term_list):
    terms = [t[0] for t in term_list]
    return terms

date = "19-05-2025" # UPDATE WITH NEW DATA
num_topics = 20 # UPDATE WITH RELEVANT # OF TOPICS

sites = ["oushinet_" + date + "-recent_gen",
         "chinanews_" + date + "-recent_gen",
         "yidali-huarenjie_" + date + "-recent_gen",
         "ihuawen_" + date + "-recent_gen"]
#sites = ["oushinet_" + date + "-recent_gen"]

# Collect information from each site
for s in sites:
    # Load text files and get list of times
    print(s)
    csv_file = pd.read_csv("../DATA/csv_files/" + s.replace("_gen", "") + ".csv")
    times = list(set([datetime.strptime(d.replace("_", " "),"%Y-%m-%d %H-%M") for d in csv_file["datetime"].tolist()]))
    times.sort()
    times = [t.strftime("%m/%d/%Y, %H:%M:%S") for t in times]

    # Load topic matrix and topic terms
    data = np.load("../DATA/topic_matrices/" + s + "_" + str(num_topics) + ".npy")
    print(data.shape)
    with open("../DATA/topic_terms/" + s + "_" + str(num_topics) + ".json") as f:
        terms = json.load(f)

    # Create rows of topic information for each datetime
    rows = []
    for i in range(len(times)):
        time = times[i]
        term_set = [", ".join(get_terms(t[1])) for t in terms[i]]
        importance_set = [round(d*100, 2) for d in data[i]]

        row = [time] + list(chain.from_iterable([[term_set[j], importance_set[j]] for j in range(num_topics)]))
        rows.append(row)

    # Create list of headers for file
    header = ["Date & Time"]
    for i in range(num_topics):
        header.append("Topic " + str(i) + " – Terms")
        header.append("Topic " + str(i) + " – Importance")

    # Create dataframe and save as excel spreadsheet
    df = pd.DataFrame(rows, columns=header)
    df.to_excel("../DATA/excel_summaries/" + s + "_" + str(num_topics) + ".xlsx", index=False)
