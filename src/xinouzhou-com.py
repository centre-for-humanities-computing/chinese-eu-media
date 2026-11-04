from bs4 import BeautifulSoup
import pandas as pd
import random
import os
import re

date = "19-05-2025" # UPDATE WITH NEW DATA

folder_path = "../DATA/xinouzhou.com_" + date

# Loop through all date folders
datetime_to_id_to_text = {}
for date_folder in os.listdir(folder_path):
    if date_folder != ".DS_Store":
        for file in os.listdir(folder_path + "/" + date_folder):
            if file.endswith(".html") and "detail-" in file:
                # Parse contents of relevant html files
                print(file)
                html = open(folder_path + "/" + date_folder + "/" + file)
                parsed_html = BeautifulSoup(html, features="lxml")
                title = parsed_html.head.title.text.split("-")[0].strip()
                body = parsed_html.find("div", {"class": "entry-content"})

                text = ""
                if body:
                    for child in body.findChildren():
                        if child.name == "p":
                            text += " " + child.text

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
df.to_csv("../DATA/csv_files/xinozhou_" + date + ".csv", index=False)
