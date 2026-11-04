from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import random
import os
import re

date = "19-05-2025" # UPDATE WITH NEW DATA

folder_path = "../DATA/ihuawen.com_" + date

# Loop through all date folders
datetime_to_id_to_text = {}
id_sources = {}
l = lambda x: datetime(*[int(_) for _ in x.split('_')[::-1]])
start = l("30_04_2024")
end = l("27_3_2025")
for date_folder in sorted(os.listdir(folder_path)):
    print(date_folder)
    if date_folder!=".DS_Store":
        time = datetime.strptime(date_folder, "%Y-%m-%d_%H-%M")
        if time < start:
            print("Too early!")
        elif time > end:
            print("Too late!")
        else:
            # Find list of articles on homepage
            html = open(folder_path + "/" + date_folder + "/index.html")
            parsed_html = BeautifulSoup(html, features="lxml")
            str_html = str(parsed_html)
            articles = re.findall(r"/article/index/id/[0-9]+", str_html)
            articles = [a.replace("/article/index/id/", "") for a in articles]

            id_sources[date_folder] = {"index": articles}

            # Find articles in subpages
            for file in os.listdir(folder_path + "/" + date_folder + "/id"):
                if file.endswith(".html") and "index" not in file:
                    id = file.replace(".html", "")
                    html = open(folder_path + "/" + date_folder + "/id/" + file)
                    parsed_html = BeautifulSoup(html, features="lxml")
                    str_html = str(parsed_html)
                    articles = re.findall(r"/article/index/id/[0-9]+", str_html)
                    articles = [a.replace("/article/index/id/", "") for a in articles]

                    id_sources[date_folder][id] = articles

            # Keep only articles in subpages of interest
            keep = []
            remove_candidates = []
            for key in id_sources[date_folder]:
                if key in ["index", "45", "69"]:
                    keep += id_sources[date_folder][key]
                else:
                    remove_candidates += id_sources[date_folder][key]

            # Find and process articles from subpages of interest
            for file in os.listdir(folder_path + "/" + date_folder):
                if file.endswith(".html") and "index" not in file:
                    id = file.replace(".html", "")
                    if id in keep:
                        html = open(folder_path + "/" + date_folder + "/" + file)
                        parsed_html = BeautifulSoup(html, features="lxml")
                        title = parsed_html.title.text.replace(" 今日华闻", "")
                        body = parsed_html.find("div", {"id": "article_content"})

                        text = body.text.strip()
                        text = ' '.join(text.split())
                        text = re.sub(' +', ' ', text)

                        if date_folder not in datetime_to_id_to_text:
                            datetime_to_id_to_text[date_folder] = {}

                        datetime_to_id_to_text[date_folder][file] = {"title": title, "text": text.strip()}

# Transform articles to dataframe format. Can determine which dates to add to final file here.
rows = []
for datetime in datetime_to_id_to_text:
    for file in datetime_to_id_to_text[datetime]:
        row = [datetime, file, datetime_to_id_to_text[datetime][file]["title"], datetime_to_id_to_text[datetime][file]["text"]]
        rows.append(row)

# Output articles in text format as dataframe
headers = ["datetime", "file", "title", "text"]
df = pd.DataFrame(rows, columns=headers)
df.to_csv("../DATA/csv_files/ihuawen_" + date + ".csv", index=False)
