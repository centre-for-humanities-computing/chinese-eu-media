import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager
from datetime import datetime
import copy

# Set font for Chinese script
matplotlib.rcParams['font.family'] = 'Heiti TC'

num_topics = 10 # UPDATE WITH RELEVANT # OF TOPICS
date = "19-05-2025" # UPDATE WITH NEW DATA

colors = {"xinouzhou_" + date + "_gen": "#ac3986",
          "chinanews_" + date + "_gen": "#f0b342",
          "ihuawen_" + date + "_gen": "#ee6f2b",
          "oushinet_" + date + "_gen": "#2f99b6",
          "yidali-huarenjie_" + date + "_gen": "#87c5a1",
          "all_data": "#e963c7"}

# Create figure with subplots and set titles
fig, axs = plt.subplots(5, 2, figsize=(30, 20), sharex=True)
axs[0][0].set_title("Novelty", fontsize=40, pad=20)
axs[0][1].set_title("Resonance", fontsize=40, pad=20)

# Loop through every source and add novelty and resonance curves for each site
files = ["xinouzhou_" + date + "_gen",
         "oushinet_" + date + "_gen",
         "chinanews_" + date + "_gen",
         "ihuawen_" + date + "_gen",
         "yidali-huarenjie_" + date + "_gen"]

for i in range(len(files)):
    df = pd.read_csv("../DATA/news_flux_output/" + files[i] + "_topic_" + str(num_topics) + "-phase3.csv")
    smooth_df = pd.read_csv("../DATA/news_flux_output/" + files[i]  + "_smoothed_56_topic_" + str(num_topics) + "-phase3.csv")

    x = df['date'].tolist()
    x = [datetime.strptime(d,"%Y-%m-%d_%H-%M") for d in x]
    y_res = df['resonance'].tolist()
    y_res_smoothed = smooth_df['smoothed_resonance']
    #changepoints_res = get_changepoints(df, 'resonance')

    y_nov = df['novelty'].tolist()
    y_nov_smoothed = smooth_df['smoothed_novelty']
    #changepoints_nov = get_changepoints(df, 'novelty')

    axs[i][0].plot(x, y_nov, color=colors[files[i]], alpha=0.8, linewidth=2, label=" ".join(files[i].split("_")[0].split("-")).title())
    axs[i][0].plot(x, y_nov_smoothed, color='black', linewidth=4)

    axs[i][1].plot(x, y_res, color=colors[files[i]], linewidth=2, alpha=0.8)
    axs[i][1].plot(x, y_res_smoothed, color='black', linewidth=4)

    # Add events of interest to plots
    #   EU parliamentary elections
    #axs[i][0].axvspan(datetime(2024, 6, 6, 0, 15), datetime(2024, 6, 10, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 6, 6, 0, 15), datetime(2024, 6, 9, 18, 15), alpha=0.5, color='#d9d9d9')

    #   UK general election
    #axs[i][0].axvspan(datetime(2024, 7, 4, 0, 15), datetime(2024, 7, 5, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 7, 4, 0, 15), datetime(2024, 7, 5, 0, 15), alpha=0.5, color='#d9d9d9')

    #   French parliamentary elections
    #axs[i][0].axvspan(datetime(2024, 6, 30, 0, 15), datetime(2024, 7, 1, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][0].axvspan(datetime(2024, 7, 7, 0, 15), datetime(2024, 7, 8, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 6, 30, 0, 15), datetime(2024, 7, 1, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 7, 7, 0, 15), datetime(2024, 7, 8, 0, 15), alpha=0.5, color='#d9d9d9')

    #   Austrian general election
    #axs[i][0].axvspan(datetime(2024, 9, 28, 0, 15), datetime(2024, 9, 29, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 9, 28, 0, 15), datetime(2024, 9, 29, 0, 15), alpha=0.5, color='#d9d9d9')

    #  Bulgarian general election
    #axs[i][0].axvspan(datetime(2024, 10, 27, 0, 15), datetime(2024, 10, 28, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 10, 27, 0, 15), datetime(2024, 10, 28, 0, 15), alpha=0.5, color='#d9d9d9')

    #   US general election
    #axs[i][0].axvspan(datetime(2024, 11, 4, 0, 15), datetime(2024, 11, 5, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2024, 11, 4, 0, 15), datetime(2024, 11, 5, 0, 15), alpha=0.5, color='#d9d9d9')

    # Germany Federal Election
    axs[i][0].axvspan(datetime(2025, 2, 23, 0, 15), datetime(2025, 2, 24, 0, 15), alpha=0.5, color='#d9d9d9')
    axs[i][1].axvspan(datetime(2025, 2, 23, 0, 15), datetime(2025, 2, 24, 0, 15), alpha=0.5, color='#d9d9d9')

    #  Poland General Election + Romania + Croatia
    #axs[i][0].axvspan(datetime(2025, 5, 18, 0, 15), datetime(2025, 5, 19, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2025, 5, 18, 0, 15), datetime(2025, 5, 19, 0, 15), alpha=0.5, color='#d9d9d9')
    # Poland 2nd round
    #axs[i][0].axvspan(datetime(2025, 6, 1, 0, 15), datetime(2025, 6, 2, 0, 15), alpha=0.5, color='#d9d9d9')
    #axs[i][1].axvspan(datetime(2025, 6, 1, 0, 15), datetime(2025, 6, 2, 0, 15), alpha=0.5, color='#d9d9d9')


    axs[i][0].tick_params(axis='both', which='both', labelsize=18)
    axs[i][1].tick_params(axis='both', which='both', labelsize=18)

# Set dates on x-axis
locator = mdates.DayLocator(interval=14)
date_form = mdates.DateFormatter("%Y-%m-%d")
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(date_form)
plt.gcf().autofmt_xdate()


# Create legend
handles = []
labels = []
for i in range(len(files)):
    h, l = axs[i][0].get_legend_handles_labels()
    handles.extend(h)
    labels.extend(l)
handles = [copy.copy(ha) for ha in handles]
[ha.set_linewidth(20) for ha in handles]
fig.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=5, frameon=False, fontsize=30)

# Save figure
fig.tight_layout()
plt.savefig("../DATA/figures/novelty_resonance_" + str(num_topics) + ".pdf", bbox_inches='tight')
plt.close()
