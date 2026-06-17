# Challenge or Empower: Revisiting Argumentation Quality in a News Editorial Corpus

Reproduction code for the CoNLL 2018 paper:

```bibtex
@inproceedings{elbaff:2018,
    title     = "Challenge or Empower: Revisiting Argumentation Quality in a News Editorial Corpus",
    author    = "El Baff, Roxanne and Wachsmuth, Henning and Al-Khatib, Khalid and Stein, Benno",
    editor    = "Korhonen, Anna and Titov, Ivan",
    booktitle = "Proceedings of the 22nd Conference on Computational Natural Language Learning",
    month     = oct,
    year      = "2018",
    address   = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url       = "https://aclanthology.org/K18-1044/",
    doi       = "10.18653/v1/K18-1044",
    pages     = "454--464"
}
```

---

## Overview

This repository contains the annotation data and analysis code used in the paper. The study investigates how readers with different political orientations (liberal vs. conservative) perceive the argumentation quality of New York Times editorials — specifically whether an editorial **challenges**, **has no effect on**, or **reinforces** their pre-existing stance.

> **Note on the NYT corpus:** The article text files (`.txt`) are derived from the New York Times Annotated Corpus, which requires a license. They are excluded from this repository. All annotation data needed to reproduce the paper's results is included.

---

## Repository Structure

```
.
├── data/
│   ├── annotations/
│   │   ├── annotations_latest.csv      # 6090 raw crowd annotations
│   │   └── personality_traits.csv      # Big Five traits for 24 annotators
│   ├── batch1/ … batch5/               # Editorial IDs per batch (txt filenames)
│   └── pilot_study/
│       ├── pilot_study.csv             # Pilot annotations (anonymized)
│       └── annotator_mapping.csv       # Anonymization mapping (pilot_ann_* codes)
├── src/conll2018_editorial_effect/     # Python package
│   ├── config.py                       # Paths, batch lists, constants
│   ├── data/
│   │   ├── loader.py                   # CSV loaders
│   │   ├── preprocessing.py            # Feature engineering per annotation row
│   │   └── batch.py                    # ARCHIVE: batch creation (requires NYT corpus)
│   ├── analysis/
│   │   ├── agreement.py                # Fleiss kappa, Cohen's kappa, Krippendorff's alpha
│   │   ├── quality.py                  # Majority-vote editorial labels, quality stats
│   │   ├── statistics.py               # Hypothesis tests (Mann-Whitney, Kruskal-Wallis, binomial)
│   │   └── correlation.py              # Spearman and Kendall tau correlations
│   └── utils/
│       └── files.py                    # Write explanation text files
├── experiments/
│   └── main.py                         # Full reproduction pipeline (run this)
├── pyproject.toml
└── .python-version                     # Pins Python 3.8 for uv
```

---

## Environment

The original analysis was written in **Python 3.6.3** (2018). The reproduction code targets **Python 3.8** and has been updated for API changes in modern `pandas` (≥ 1.0) and `scipy` (≥ 1.9). The locked dependency versions are in `uv.lock`.

Dependencies are managed with [uv](https://docs.astral.sh/uv/). Install it with:

```bash
pip install uv
# or: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd conll2018_editorial_effect

# Create the virtual environment and install all dependencies
# uv reads .python-version (3.8) and uv.lock automatically
uv sync
```

That single command creates `.venv/` with Python 3.8.20 and all pinned packages.

### Run

```bash
uv run python experiments/main.py
```

Or, if the virtualenv is already activated:

```bash
python experiments/main.py
```

The script prints all results to stdout in labelled sections. Compare the printed values to the tables and figures in the paper.

---

## Data Description

### Annotation CSV (`data/annotations/annotations_latest.csv`)

Each row is one annotation by one crowd worker for one editorial.

| Column            | Description |
|-------------------|-------------|
| `annotator_id`    | ID. Prefix `L` = liberal, `C` = conservative (see below). |
| `article_id`      | NYT article filename (e.g. `1638699.txt`). |
| `political_typology` | Pew Research Center category (e.g. "Country First Conservatives"). |
| `effect`          | Effect rating on a 1–5 scale (see scale below). |
| `explanation`     | Free-text justification written by the annotator. |
| `article_index`   | Position of the article in the annotator's task. |
| `change`          | Whether the editorial changed the annotator's mind (`YES`/`NO`). |
| `reinforce`       | Whether the editorial reinforced the annotator's stance (`YES`/`NO`). |
| `date_created`    | Timestamp of submission. |

**Effect scale (1–5):**

| Value | Meaning |
|-------|---------|
| 1 | Strongly challenged my stance |
| 2 | Somewhat challenged my stance |
| 3 | Neither challenged nor reinforced (no effect) |
| 4 | Somewhat reinforced my stance |
| 5 | Strongly reinforced my stance |

**Abstracted effect (1–3):** used in most analyses:

| Abstracted | Original | Label |
|------------|----------|-------|
| 1 | 1 or 2 | Challenging |
| 2 | 3 | No effect |
| 3 | 4 or 5 | Reinforcing |

### Personality Traits (`data/annotations/personality_traits.csv`)

Big Five personality scores for the 24 annotators, collected via the Pew Research Center Big Five test.

| Column | Values | Meaning |
|--------|--------|---------|
| `ID` | e.g. `L01`, `C03` | Annotator ID |
| `extraversion` … `openness` | `LOW` / `AVERAGE` / `HIGH` | Trait level (coded 1/2/3 in analysis) |

---

## Experiments

### Annotators and Political Orientation

24 annotators were recruited via Upwork. Each annotator completed the [Pew Research Center Political Typology Quiz](https://www.pewresearch.org/politics/quiz/political-typology/) before the annotation task. Their quiz result determined their political group:

- **Liberal** — annotator ID prefix `L` (12 annotators)
- **Conservative** — annotator ID prefix `C` (12 annotators)

### Batches

Annotators were assigned to one of four batches. Each batch contains 6 annotators (3 liberal, 3 conservative), each rating 250 articles. Articles are non-overlapping across batches.

| Batch  | Conservatives       | Liberals            | Articles |
|--------|--------------------|--------------------|----------|
| batch1 | C03, C09, C11      | L01, L03, L07      | 250      |
| batch2 | C02, C07, C12      | L08, L14, L15      | 250      |
| batch3 | C04, C10, C14      | L05, L11, L12      | 250      |
| batch4 | C06, C13, C15      | L04, L06, L09      | 250      |

**Total:** 6 annotators × 1000 articles = **6000 annotations** across 1000 editorials.

> Batch 5 was used during data collection for pilot/backup purposes. Its articles are redistributed across batches 1–4 in the final dataset.

---

## Reproduction Steps

`experiments/main.py` runs the full pipeline in order. Each step is described below.

### Step 1 — Load Data

Loads `annotations_latest.csv` (6090 rows) and `personality_traits.csv` (24 rows).

### Step 2 — Preprocessing

Applied per annotation row:

1. **Political pole** — derived from annotator ID prefix: `L` → `liberal`, `C` → `conservative`.
2. **Effect abstraction** — maps the 1–5 scale to 1–3 (challenging / no effect / reinforcing).
3. **Batch assignment** — assigned by annotator ID using the batch lists in `config.py`.
4. **Intensity** — `strong` (effect 1 or 5), `moderate` (effect 2 or 4), `none` (effect 3).
5. **Has effect** — binary flag: 1 if effect is challenging or reinforcing, 0 if no effect.
6. **Personality traits** — joined from `personality_traits.csv` on annotator ID; LOW/AVERAGE/HIGH mapped to 1/2/3.

After removing 90 duplicate (annotator, article) pairs and filtering annotators who dropped out mid-study, **6000 annotations** remain: 3000 liberal and 3000 conservative.

Assertions verified at this step:
- 6000 total annotations (3000 liberal, 3000 conservative)
- 1000 unique articles, 24 unique annotators, 4 batches
- `effect` values in [1, 5], `effect_abstracted` values in {1, 2, 3}
- No duplicate (annotator, article) pairs

### Step 3 — Save JSON

Exports the preprocessed 6000-row DataFrame to `data/annotations/conll2018_data.json`.

### Step 4 — Inter-Rater Agreement: Fleiss Kappa and Krippendorff's Alpha (NLTK)

Calculated **per batch** (each batch: 6 annotators × 250 articles). Passing all annotators at once is not valid because each annotator only rated their own batch's 250 articles — the full annotation matrix is incomplete.

Three agreement measures are reported:

- **Fleiss kappa** (`multi_kappa`) — multi-annotator generalisation of Cohen's kappa; assumes all raters rate all items within the batch.
- **Krippendorff's alpha** (`alpha`) — accounts for missing data and supports ordinal measurement.
- **Cohen's kappa** — pairwise; reported as the average over all pairs within each batch.

Reported for:
- Effect abstracted (1–3): conservatives, liberals, all annotators
- Has effect (binary): conservatives, liberals, all annotators
- Both overall (averaged across batches) and pairwise (averaged over all annotator pairs per batch)

### Step 5 — Krippendorff's Alpha (ordinal, `krippendorff` library)

Uses the `krippendorff` library directly, which supports the ordinal distance metric. Reported for:

- Effect 1–5 and effect abstracted 1–3
- All annotators, liberals only, conservatives only
- Overall and per batch

Also reports **pairwise Krippendorff's alpha** averaged over all annotator pairs within each batch.

### Step 6 — Majority and Full Agreement

Simple agreement metrics at the per-article level, within each political group:

- **Majority agreement** — fraction of annotations matching the group majority vote.
- **Full agreement** — fraction of articles where all 3 annotators in the group gave the same label.

Reported for effect 1–5 and effect abstracted 1–3.

### Step 7 — Editorial Quality: Majority Vote Labels

For each article, an editorial-level label is computed **separately for each political group** using **majority vote among the 3 annotators in that group**:

- If at least 2 of the 3 annotators agree → majority label = that value.
- If all 3 disagree (every vote is unique, max count = 1) → no majority; label coded as 0.

This produces two labels per article — one for the liberal group, one for the conservative group — and reports the joint distribution:

| Combination | Example interpretation |
|------------|----------------------|
| CHALLENGING–REINFORCING | Liberal group: challenged; Conservative group: reinforced |
| CHALLENGING–CHALLENGING | Both groups: challenged |
| REINFORCING–REINFORCING | Both groups: reinforced |
| REINFORCING–NO EFFECT | One group: reinforced; other: no effect |
| etc. | |

242 of 1000 articles had no majority in at least one group.

### Step 8 — Hypothesis Testing

Tests whether effect ratings differ significantly across political groups or between individual annotators:

- **Mann-Whitney U** — tests if the distribution of effect ratings differs between liberals and conservatives (non-parametric; ordinal data, 2 groups).
- **Kruskal-Wallis** — tests if the distribution differs across the 3 individual annotators within conservatives or within liberals (non-parametric; ordinal data, >2 groups).

Run for both effect 1–5 and effect abstracted 1–3. Normality is checked first via the Shapiro-Wilk test; all groups are non-normally distributed, confirming the choice of non-parametric tests.

- **Wilcoxon signed-rank** — tests if the reinforcing counts differ between liberal and conservative groups at the article level.

### Step 9 — Spearman Correlation: Liberal vs. Conservative View

Spearman's rho between the liberal and conservative majority-vote labels across 1000 articles, for combinations including challenging, reinforcing, has-effect, and the raw majority vote.

### Step 10 — Correlation: Personality Traits

Spearman's rho and Kendall's tau between each Big Five trait (extraversion, agreeableness, conscientiousness, neuroticism, openness) and annotation outcome columns (effect abstracted, challenging, reinforcing, has effect). Reported for liberals, conservatives, and all annotators combined.

### Step 11 — Personality Trait Distribution

Count of annotators per trait level (LOW / AVERAGE / HIGH), broken down by political group.

### Step 12 — Write Explanation Files

Exports annotator free-text explanations grouped by abstracted effect label to:
(already saved no need to run). These files were inspected by the authors.
- `data/explanations_challenging.txt`
- `data/explanations_noeffect.txt`
- `data/explanations_reinforcing.txt`

---

## Contact

For questions about the annotation data or the analysis code, contact **Roxanne El Baff** at roxanne.elbaff@gmail.com.
