import pandas as pd

from conll2018_editorial_effect.config import (
    data_file_path,
    data_all_json,
    personality_path,
)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 2
# Change: wrapped in a function
# -----------------------------------------------------------------------
def load_annotations():
    data_df = pd.read_csv(data_file_path, sep=",")
    return data_df


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 3
# Change: wrapped in a function
# Change: renamed columns after load — CSV has 'ID' (uppercase), mixed-case
#         trait names (Conscientiousness/Neuroticism/Openness), and a
#         duplicate 'extraversion' column (numeric at pos 1, string LOW/HIGH/AVERAGE
#         at pos 6). Positional rename resolves all three issues.
# -----------------------------------------------------------------------
def load_personality_traits():
    data_personality_df = pd.read_csv(personality_path, sep=",")
    data_personality_df.columns = [
        'id', 'extraversion_num', 'agreeableness_num', 'conscientiousness_num',
        'neuroticism_num', 'openness_num',
        'extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness',
    ]
    # Change: normalize annotator IDs to zero-padded form (e.g. C3->C03, C9->C09)
    #         so they match the format used in annotations_latest.csv and config.py batch lists
    data_personality_df['id'] = data_personality_df['id'].apply(
        lambda x: x[0] + x[1:].zfill(2)
    )
    return data_personality_df


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 5
# Change: wrapped in a function; data_batch_json removed (commented out in config)
# -----------------------------------------------------------------------
def save_annotations_json(data_df):
    tmp_all = data_df[(data_df["batch"].notnull())]
    print(len(tmp_all))
    tmp_all.to_json(path_or_buf=data_all_json, orient="records")


# -----------------------------------------------------------------------
# Source: inter-rater-agreement.ipynb, cell 6
# Change: wrapped in a function; path moved to argument
# -----------------------------------------------------------------------
def load_pilot_study(path_emnlp2018_pilotstudy):
    pilot_emnlp2018 = pd.read_csv(path_emnlp2018_pilotstudy, sep=",")
    pilot_emnlp2018 = pilot_emnlp2018[
        ["article ID", "name", "political typology", "affect"]
    ]

    user_map = {
        "pilot_ann_5": "PL01",
        "pilot_ann_3": "PC01",
        "pilot_ann_4": "PL02",
        "pilot_ann_7": "PC02",
        "pilot_ann_6": "PC03",
        "pilot_ann_1": "PL03",
    }

    effect_dict = {
        "It somehow reinforced my stance": 4,
        "It somehow challenged me": 2,
        "It neither challenged me nor reinforced my stance": 3,
        "It strongly reinforced my stance": 5,
        "It strongly challenged me": 1,
    }

    def add_user_id(row):
        row["annotator_id"] = user_map[row["name"].strip()]
        if row["annotator_id"].startswith("PL"):
            row["political_group"] = "liberal"
        else:
            row["political_group"] = "conservative"

        row["effect_num"] = effect_dict[row["affect"].strip()]
        if row["effect_num"] == 5 or row["effect_num"] == 4:
            row["effect_abstract"] = 3
        if row["effect_num"] == 1 or row["effect_num"] == 2:
            row["effect_abstract"] = 1
        if row["effect_num"] == 3:
            row["effect_abstract"] = 2
        return row

    pilot_emnlp2018 = pilot_emnlp2018[pilot_emnlp2018["name"] != "pilot_ann_2"]
    pilot_emnlp2018 = pilot_emnlp2018.apply(add_user_id, axis=1)

    liberal_df = pilot_emnlp2018[pilot_emnlp2018["political_group"] == "liberal"]
    conservative_df = pilot_emnlp2018[
        pilot_emnlp2018["political_group"] == "conservative"
    ]

    return pilot_emnlp2018, liberal_df, conservative_df
