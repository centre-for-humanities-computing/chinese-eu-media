import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from datetime import datetime
from matplotlib import font_manager
import seaborn as sns
import matplotlib
import numpy as np
import pandas as pd

# Set font for Chinese script
matplotlib.rcParams['font.family'] = 'Heiti TC'

date = "21-11-2024" # UPDATE WITH NEW DATA

sites = ["xinouzhou", "oushinet", "yidali-huarenjie", "chinanews", "ihuawen"]

# Create summary information from site files
unique_articles = {}
repeat_articles = {}
all_articles = {}
new_articles = {}
system_dates = []
for s in sites:
    df = pd.read_csv("../DATA/csv_files/" + s + "_" + date + ".csv")

    # Get all and unique articles
    all_article_names = df["file"].tolist()
    unique_article_names = df["file"].unique().tolist()
    repeat_counts = [all_article_names.count(a) for a in unique_article_names]

    repeat_articles[s] = np.mean(repeat_counts)
    unique_articles[s] = len(df["file"].unique().tolist())
    all_articles[s] = len(df["file"].tolist())

    dates = df["datetime"].unique().tolist()
    dates = sorted(dates, key=lambda x: datetime.strptime(x, '%Y-%m-%d_%H-%M'))

    system_dates = dates

    # Get # of new articles by datetime
    last_set = []
    num_new_articles = {}
    for d in dates:
        d_df = df[df["datetime"] == d]
        article_set = d_df["file"].unique().tolist()

        num_new = len([a for a in article_set if a not in last_set])
        num_new_articles[d] = num_new
        last_set = article_set
    new_articles[s] = num_new_articles

# Get list of unique and total # articles
uniques = [unique_articles[s] for s in sites]
alls = [all_articles[s] for s in sites]

# Fix misspelling
sites[0] = "xinouzhou"

# Fix site titles
nice_sites = [s.replace("-", " ").title() for s in sites]

# Reverse data lists
uniques.reverse()
alls.reverse()
nice_sites.reverse()

# Plot the # of total an unique articles by site
fig, ax = plt.subplots(figsize=(20,8))

total_bars = plt.barh(nice_sites, alls, label='Total', color="#ac3986")
unique_bars = plt.barh(nice_sites, uniques, label='Unique', color="#d279b5", edgecolor="white")

ax.bar_label(total_bars, padding=6, color='black', fmt='{:,.0f}', fontsize=12, label_type='edge', fontweight='bold')
ax.bar_label(unique_bars, padding=6, color='white', fmt='{:,.0f}', fontsize=12, label_type='edge', fontweight='bold')

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.xlim([0,175000])
plt.ylabel('News Site', labelpad=8, fontsize=18)
plt.xlabel('# Articles', labelpad=8, fontsize=18)
plt.title('Total and Unique Articles Collected by Site', fontsize=20, pad=12)

plt.legend(loc='best', fontsize=14)
plt.savefig("../DATA/figures/dataset_total_unique.pdf", bbox_inches='tight')

# Create a nested list of the # new articles by date by site
all_points = []
for s in new_articles:
    points = []
    for d in system_dates:
        if d in new_articles[s]:
            points.append(new_articles[s][d])
        else:
            points.append(0)
    all_points.append(points)

# Plot the # of new articles per day for each site
fig, axs = plt.subplots(5, 1, figsize=(12, 12), sharex=True)

axs[0].plot(system_dates, all_points[0], color='#7a295f', label="Xinouzhou")
axs[0].legend(loc='upper right', fontsize=14)
axs[0].set_title('# New Articles at Each Time Point', fontsize=24, pad=10)

axs[1].plot(system_dates, all_points[1], color='#1f677a', label="Oushinet")
axs[1].legend(loc='upper right', fontsize=14)

axs[2].plot(system_dates, all_points[2], color='#5AAF7D', label="Yidali Huarenjie")
axs[2].legend(loc='upper right', fontsize=14)
axs[2].set_ylabel("# New Articles", fontsize=18, labelpad=8)

axs[3].plot(system_dates, all_points[3], color='#e79d13', label="Chinanews")
axs[3].legend(loc='upper right', fontsize=14)

axs[4].plot(system_dates, all_points[4], color='#d05411', label="Ihuawen")
axs[4].legend(loc='upper right', fontsize=14)
axs[4].set_xlabel("Date", fontsize=18, labelpad=8)

fig.tight_layout()
plt.xticks(fontsize=8)
plt.setp(axs, xticklabels=[])

plt.savefig("../DATA/figures/new_articles.pdf", bbox_inches='tight')
plt.close()
