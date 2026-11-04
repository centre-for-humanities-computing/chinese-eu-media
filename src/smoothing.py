import os
import sys
import argparse
import pandas as pd

# Code from newsFluxus Github
path = os.path.join("newsFluxus", "src")
sys.path.append(path)

import news_uncertainty

date = "19-05-2025" # UPDATE WITH NEW DATA
num_topics = 10 # UPDATE WITH RELEVANT # OF TOPICS
span = 56  # 56 IS VALUE FROM EMODYNAMICS – CAN BE CHANGED

files = ["xinouzhou_" + date + "_gen",
         "chinanews_" + date + "_gen",
         "yidali-huarenjie_" + date + "_gen",
         "ihuawen_" + date + "_gen",
         "oushinet_" + date + "_gen"]

# Smooth the transience, novelty, and resonance signals from each source
for f in files:
    print(f)
    filepath = "../DATA/news_flux_output/" + f + "_topic_" + str(num_topics) + "-phase3.csv"
    outpath = "../DATA/news_flux_output/" + f + "_smoothed_" + str(span) + "_topic_" + str(num_topics) + "-phase3.csv"

    df = pd.read_csv(filepath)
    df["smoothed_transience"] = news_uncertainty.adaptive_filter(df["transience"], span=span)
    df["smoothed_novelty"] = news_uncertainty.adaptive_filter(df["novelty"], span=span)
    df["smoothed_resonance"] = news_uncertainty.adaptive_filter(df["resonance"], span=span)

    df.to_csv(outpath, index=False)
