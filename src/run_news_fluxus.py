import json
from datetime import datetime
import numpy as np
import pandas as pd
import os, sys

# Code from newsFluxus Github
path = os.path.join("newsFluxus", "src")
sys.path.append(path)

from main_extractor import extract_novelty_resonance

date = "19-05-2025" # UPDATE WITH NEW DATA
num_topics = 10 # UPDATE WITH RELEVANT # OF TOPICS

# Run the news fluxus pipeline on the embeddings for each datasource
files = ["xinouzhou_" + date + "_gen",
         "chinanews_" + date + "_gen",
         "yidali-huarenjie_" + date + "_gen",
         "ihuawen_" + date + "_gen",
         "oushinet_" + date + "_gen"]

#files = ["oushinet_" + date + "_gen"]

for f in files:
    print(f"Reading {f}...")
    csv_file = pd.read_csv("../DATA/csv_files/" +
                           f.replace("_gen", "") +
                           ".csv")

    times = csv_file["datetime"].tolist()
    #times = [datetime.strptime(d.replace("_", " "),"%Y-%m-%d %H-%M") for d in times]
    dates = list(set(times))
    dates.sort()

    embeds = list(np.load("../DATA/topic_matrices/" + f + "_" + str(num_topics) + ".npy"))

    df_phase1 = pd.DataFrame()
    df_phase1["date"] = dates
    df_phase1["embed"] = embeds

    ids = [idx for idx, row in df_phase1.iterrows() if row["date"]>"2025-01-31" and row["date"]<"2025-03-21"]
    df_phase1 = df_phase1.iloc[ids]
    embeds_phase1 = [embeds[idx] for idx in ids]
    dates_phase1 = [dates[idx] for idx in ids]

    df_phase1 = extract_novelty_resonance(df_phase1,
                                          embeds_phase1,
                                          dates_phase1,
                                          12) # THREE IS VALUE FROM EMODYNAMICS – CAN BE CHANGED
    df_phase1.to_csv("../DATA/news_flux_output/" +
              f +
              "_topic_" +
              str(num_topics) +
              "-phase3" +
              ".csv",
              index=False)
