# Data

## Available data

| Path | Description |
|---|---|
| `results/figures/topic_importance_*.png` | Topic importance over time for *Nouvelles d'Europe* (NE), all phases combined and per phase |
| `results/topic_models/oushinet_phase3/{10,20}_topics/doc_topic_distributions_*.csv.gz` | Document–topic weights for every NE article in every phase 3 snapshot |
| `results/topic_models/oushinet_phase3/{10,20}_topics/topic_labels_*.csv` | Topic labels, English glosses, primary-topic shares |
| `results/topic_models/oushinet_phase3/20_topics/topics_over_time_20.html` | Interactive Plotly chart from turftopic's `plot_topics_over_time()` for the 20-topic dynamic model |

The 10-topic model is the one reported in the article. The 20-topic model is included for comparison.

The document–topic distributions come from `extract_doc_topics.py`. That script fits a *static* KeyNMF model to the saved keyword scores, whereas the figures come from the *dynamic* model in `run_turftopic10.py`. Both use the same keyword matrix, but topic indices are not guaranteed to line up across the two fits.

## Data not made available

- **Article text and titles.** Article texts are copyrighted by NE and are not redistributed. The released tables identify articles by NE's article ID and snapshot timestamp only.
- **Raw scrape, parsed CSV corpus, embeddings, keyword files.** These either contain the article text or can be used to reconstruct it closely. They are kept on UCloud, Aarhus University's secure GDPR-compliant research infrastructure.
- **Data from other outlets** (xinouzhou, chinanews.se, yidali.huarenjie, ihuawen). The parsing code is included, but the published article analyses NE only.

Researchers who want access to restricted material to verify the results should contact the authors.

## Column dictionary

### `doc_topic_distributions_{10,20}.csv.gz`

| Column | Type | Description |
|---|---|---|
| `snapshot` | string, `YYYY-MM-DD_HH-MM` | Time of the six-hourly scrape in which the article was linked from the site |
| `article_id` | string | NE's article identifier (the HTML filename in the scrape, without `.html`) |
| `topic_0` … `topic_{k-1}` | float ≥ 0 | KeyNMF document–topic weight. Weights are not normalised to sum to 1. |

Each row is one article in one snapshot. An article that stays on the site across several snapshots therefore appears several times. Coverage:

| | 10 topics | 20 topics |
|---|---|---|
| Rows | 84,523 | 84,523 |
| Unique articles | 5,390 | 5,390 |
| Snapshots | 504 | 504 |
| First snapshot | 2024-11-21 00:15 | 2024-11-21 00:15 |
| Last snapshot | 2025-03-26 18:15 | 2025-03-26 18:15 |

Weights are the same in every snapshot for 5,375 of the 5,390 articles. The other 15 differ slightly, most likely because the article text was edited between scrapes. In one case the primary topic changes.

The file extends past 28 February 2025, the end of the window analysed in the article. To restrict to that window, filter on `snapshot < "2025-03-01"`.

### `topic_labels_{10,20}.csv`

| Column | Description |
|---|---|
| `topic` | Topic index, matching `topic_<i>` in the distributions file |
| `label_zh` | The four highest-ranked keywords, as produced by turftopic |
| `gloss_en` | Our English gloss of those keywords, for orientation only |
| `primary_share_pct` | Percentage of unique articles (first snapshot in which each appears) for which this topic has the highest weight |

### Reading the files

```python
import pandas as pd

dist = pd.read_csv("results/topic_models/oushinet_phase3/10_topics/doc_topic_distributions_10.csv.gz",
                   dtype={"article_id": str})
labels = pd.read_csv("results/topic_models/oushinet_phase3/10_topics/topic_labels_10.csv")
```

Read `article_id` as a string. The IDs are 19-digit integers and lose precision if parsed as floats.
