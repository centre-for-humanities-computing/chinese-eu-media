# Pipeline

This page documents the scripts in `src/` as they were run for the article. The code has not been refactored for release. Paths, dates and other settings are hard-coded at the top of each script, marked with comments like `# UPDATE WITH NEW DATA`.

## Running context

- Scripts are run **from inside `src/`** and read and write `../DATA/`, which is a `DATA/` directory at the repository root. `DATA/` is git-ignored and not distributed (see [data.md](data.md)).
- `extract_doc_topics.py` is the one exception: it uses paths relative to the repository root (`DATA/...`) and writes to `for_mette/...`.
- `embeddings.py` and `run_turftopic*.py` load the sentence transformer with `device="mps"` (Apple silicon). On other hardware, use `"cuda"` or `"cpu"`.
- The matplotlib scripts set `font.family = 'Heiti TC'` (a macOS font) so that Chinese renders. Elsewhere, any CJK-capable font such as Noto Sans CJK will do.
- The corpus snapshot used throughout is dated `19-05-2025`. Files carrying the suffix `-recent` hold the phase 3 subset (21 November 2024 onwards).

## Expected `DATA/` layout

```
DATA/
├── oushinet.com_19-05-2025/            Raw scrape: one folder per snapshot (YYYY-MM-DD_HH-MM), HTML files inside
├── stopwords-zh.txt                    https://github.com/stopwords-iso/stopwords-zh
├── csv_files/      <site>_<date>.csv                 datetime, file, title, text
├── embeddings/     <site>_<date>_gen.npy             one row per CSV row
├── keywords/       <site>_<date>_gen_keywords{10,20}.jsonl   KeyNMF keyword scores per document
├── topic_terms/    <site>_<date>_gen_{10,20}.json    topic terms per time bin
├── topic_matrices/ <site>_<date>_gen_{10,20}.npy     temporal topic importance (time bins × topics)
├── excel_summaries/                    per-snapshot topic summaries
├── news_flux_output/                   novelty/resonance signals
└── figures/                            HTML and PDF outputs
```

## Stages

### 1. Parse scraped HTML → CSV corpus

| Script | Site | Notes |
|---|---|---|
| `oushinet-com.py` | oushinet.com (*Nouvelles d'Europe*) | **Used in the article.** Walks every snapshot folder except `channel-contents` and `logs`. Extracts `div.content_title` and `div.content_content`. |
| `xinouzhou-com.py` | xinouzhou.com | Collected but not analysed in the published article |
| `chinanews-se.py` | chinanews.se | Collected but not analysed in the published article |
| `yidali-huarenjie-com.py` | yidali.huarenjie.com | Collected but not analysed in the published article |
| `ihuawen-com.py` | ihuawen.com | Collected but not analysed in the published article. Keeps only front-page and subpage IDs 45 and 69, restricted to 30 April 2024 – 27 March 2025. |

Each script writes `DATA/csv_files/<site>_<date>.csv` with columns `datetime, file, title, text`. One row is one article in one snapshot, so an article that stays on the site across several snapshots appears once per snapshot.

### 2. Embed documents

`embeddings.py` encodes the `text` column with `paraphrase-multilingual-MiniLM-L12-v2` using a multi-process pool, and saves `DATA/embeddings/<site>_<date>_gen.npy`. The `sites` list is edited by hand to choose which corpus to embed.

### 3. Dynamic topic model

`run_turftopic10.py` (used in the article) and `run_turftopic20.py` (robustness/alternative):

1. Load the embeddings and CSV, and drop rows with no text.
2. Turn snapshot timestamps into datetimes. Each unique snapshot becomes a time bin, and a closing bin edge is appended.
3. Build a `CountVectorizer` that tokenises with `jieba.lcut` and removes stopwords-zh. This vocabulary is the pool of candidate keywords that KeyNMF scores against document embeddings.
4. `KeyNMF(n_components=10)` → `extract_keywords` (saved to `keywords/*.jsonl`) → `fit_transform_dynamic` over the time bins.
5. Save the interactive topics-over-time plot (`figures/*_time_series_10.html`), topic terms per bin (`topic_terms/*.json`) and `model.temporal_importance_` (`topic_matrices/*.npy`).

`run_turftopic10.py` is currently set to oushinet only. `run_turftopic20.py` loops over all five sites.

### 4. Document–topic distributions

`extract_doc_topics.py` reuses the saved keyword file, so no embedding model is needed. It fits a (static) `KeyNMF(n_components=10)` to the corpus and appends one column per topic to the CSV. The output is the `*_topics_distributions.xlsx` spreadsheet, from which [`results/topic_models/`](../results/topic_models) was derived by dropping the `title` and `text` columns. As committed, the script is configured for yidali-huarenjie. Edit the input and output paths to run it for another site.

### 5. Topic summaries

`gather_topic_info.py` combines `topic_matrices/*.npy` and `topic_terms/*.json` into one Excel sheet per site. Each row is a snapshot; for each topic it gives the terms and the importance in percent.

### 6. Corpus descriptives

`create_dataset_figures.py` plots total vs unique articles per site and new articles per snapshot (`dataset_total_unique.pdf`, `new_articles.pdf`). It is configured for the `21-11-2024` snapshot (phases 1–2).

### 7. Novelty and resonance (exploratory, not reported in the article)

These scripts apply the information-dynamics measures from [newsFluxus](https://github.com/centre-for-humanities-computing/newsFluxus) to the temporal topic-importance vectors:

- `run_news_fluxus.py` computes novelty, transience and resonance with window 12 for snapshots between 31 January and 21 March 2025 (`*-phase3.csv`).
- `smoothing.py` applies newsFluxus's adaptive filter with span 56.
- `figures.py` produces a 5 × 2 grid of novelty and resonance per site, with the German federal election (23 February 2025) shaded.

The scripts import from `src/newsFluxus/src/` by adding it to `sys.path` relative to the working directory.

### Not included

- The script that produced `results/figures/*.png`, including the grouping of the 10 topics into the *Europe*, *China* and *Elections* clusters shown there. **TODO: add the script, or document the topic-to-cluster mapping.**
- The scraping server itself.
- The MAXQDA project used for the qualitative framing analysis.
