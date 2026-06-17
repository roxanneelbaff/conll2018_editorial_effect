from conll2018_editorial_effect.config import (
    batch1,
    batch2,
    batch3,
    batch4,
    personality_dic,
)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 4
# Change: wrapped in a function; data_personality_df passed as argument
#         instead of global variable
# -----------------------------------------------------------------------
def add_cols(row, data_personality_df):
    # Politcal Pole
    political_pol = 'liberal'
    if row['annotator_id'].startswith('C'):
        political_pol = 'conservative'
    row['political_pole'] = political_pol

    # Abstracted Effect
    row['challenging'] = 0
    row['reinforcing'] = 0
    if row['effect'] < 3:
        row['effect_abstracted'] = 1 # means challenging
        row['challenging'] = 1
    elif row['effect'] > 3:
        row['effect_abstracted'] = 3 # means empowering
        row['reinforcing'] = 1
    else:
        row['effect_abstracted'] = 2 # No effect

    # Add batch information
    if row['annotator_id'] in batch1:
        row['batch'] = 'batch1'
    elif row['annotator_id'] in batch2:
        row['batch'] = 'batch2'
    elif row['annotator_id'] in batch3:
        row['batch'] = 'batch3'
    elif row['annotator_id'] in batch4:
        row['batch'] = 'batch4'
    else:
        row['batch'] = None

    # Add intensity
    if row['effect'] == 1 or row['effect'] == 5:
        row['intensity'] = 'strong'
    elif row['effect'] == 2 or row['effect'] == 4:
        row['intensity'] = 'moderate'
    else:
        row['intensity'] = 'none'

    # add has effect:
    row['has_effect'] = 0
    if row['effect_abstracted'] == 1 or row['effect_abstracted'] == 3:
        row['has_effect'] = 1

    # Add personality traits 'extraversion', 'agreeableness',  'conscientiousness', 'neuroticism', 'openness'
    if row['batch'] != None:
        row['extraversion'] = personality_dic[data_personality_df[data_personality_df['id'] == row['annotator_id']]['extraversion'].values[0]]
        row['agreeableness'] = personality_dic[data_personality_df[data_personality_df['id'] == row['annotator_id']]['agreeableness'].values[0]]
        row['conscientiousness'] = personality_dic[data_personality_df[data_personality_df['id'] == row['annotator_id']]['conscientiousness'].values[0]]
        row['neuroticism'] = personality_dic[data_personality_df[data_personality_df['id'] == row['annotator_id']]['neuroticism'].values[0]]
        row['openness'] = personality_dic[data_personality_df[data_personality_df['id'] == row['annotator_id']]['openness'].values[0]]
    return row


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 4 (bottom) + cell 6
# Change: wrapped in a function; data_personality_df passed as argument
# -----------------------------------------------------------------------
def preprocess(data_df, data_personality_df):
    data_df.drop_duplicates(['annotator_id', 'article_id'], keep='first', inplace=True)
    data_df = data_df.apply(lambda row: add_cols(row, data_personality_df), axis=1)

    ## REMOVE FOR FINAL CALCULTION
    data_df = data_df[ data_df['batch'].notnull() ] # Some annotators droppped, ther id is not in the list

    return data_df


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 7
# Change: wrapped in a function
# -----------------------------------------------------------------------
def split_by_political_pole(data_df):
    conservatives_df = data_df[data_df['political_pole'] == 'conservative']
    liberals_df = data_df[data_df['political_pole'] == 'liberal']
    return liberals_df, conservatives_df


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 99
# Change: wrapped in a function; data_personality_df passed as argument
#         instead of global variable
# -----------------------------------------------------------------------
def add_polit(row):
    # Politcal Pole
    political_pol = 'liberal'
    if row['id'].startswith('C'):
        political_pol = 'conservative'
    row['political_pole'] = political_pol
    return row


def add_political_pole_to_personality(data_personality_df):
    data_personality_df = data_personality_df.apply(add_polit, axis=1)
    return data_personality_df
