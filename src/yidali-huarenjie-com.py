from bs4 import BeautifulSoup
import pandas as pd
import random
import os
import re

date = "19-05-2025" # UPDATE WITH NEW DATA

folder_path = "../DATA/yidali.huarenjie.com_" + date

# Loop through all date folders
datetime_to_id_to_text = {}
for date_folder in os.listdir(folder_path):
    if date_folder != ".DS_Store":
        for file in os.listdir(folder_path + "/" + date_folder):
            print(os.path.join(folder_path, file))
            # Parse articles
            if file.endswith(".html") and "portal.php" in file:
                html = open(folder_path + "/" + date_folder + "/" + file)
                parsed_html = BeautifulSoup(html, features="lxml")
                title = parsed_html.title.text.split("-")[0].strip()

                body = parsed_html.find("td", {"id": "article_content"})

                if body:
                    text = body.text.strip()
                    text = text.split("——华人街网站 alexzou编")[0].strip()

                    text = " ".join(text.split())
                    text = re.sub(' +', ' ', text)

                    if date_folder not in datetime_to_id_to_text:
                        datetime_to_id_to_text[date_folder] = {}

                    datetime_to_id_to_text[date_folder][file] = {"title": title, "text": text.strip()}

            # Parse community threads
            elif file.endswith(".html") and "thread-" in file:
                html = open(folder_path + "/" + date_folder + "/" + file)
                parsed_html = BeautifulSoup(html, features="lxml")
                title = parsed_html.title.text.split("-")[0].strip()
                body = parsed_html.find("td", {"class": "my-first t_f"})

                if body:
                    text = body.text.strip()

                    if "\nx\n" in text:
                        text = text.split("\nx\n")[1].strip()

                    text = re.sub(r"document.getElementById[\S\s]+;", "", text)

                    text = " ".join(text.split())
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
df.to_csv("../DATA/csv_files/yidali-huarenjie_21-11-2024.csv", index=False)
