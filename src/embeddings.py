from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np


def main():
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2",
                                device="mps")

    date = "19-05-2025" # UPDATE WITH NEW DATA

    news_sites = [#"xinouzhou_" + date + ".csv",
                  #"oushinet_" + date + ".csv",
                  #"yidali-huarenjie_" + date + ".csv",
                  "ihuawen_" + date + ".csv"]
                  #"chinanews_" + date + ".csv"]

    # Embed and save the texts from each data source
    path = "../DATA/csv_files/"
    for n in news_sites:
        print(n)
        df = pd.read_csv(path + n)

        texts = df.fillna("").text.tolist()
        pool = model.start_multi_process_pool()
        embeddings = model.encode_multi_process(texts,
                                                pool,
                                                show_progress_bar=True)
        model.stop_multi_process_pool(pool)

        with open('../DATA/embeddings/' + n.replace(".csv", "") + '_gen.npy', 'wb') as f:
            np.save(f, embeddings)

if __name__=="__main__":
    main()
