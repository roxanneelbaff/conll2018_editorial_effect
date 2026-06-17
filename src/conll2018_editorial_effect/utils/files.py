# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 3
# Change: none
# -----------------------------------------------------------------------
def get_filename(path):
    return path.split('/')[-1].split('.')[0]


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 85
# Change: wrapped in a function; data_df passed as argument
# -----------------------------------------------------------------------
def write_explanations(data_df):
    with open("data/explanations_noeffect.txt", "w") as w1:
        for explanation in data_df[data_df['effect_abstracted']==2]['explanation'].values:
            w1.write(explanation+'\n\n')
    with open("data/explanations_challenging.txt", "w") as w2:
        for explanation in data_df[data_df['effect_abstracted']==1]['explanation'].values:
            w2.write(explanation+'\n\n')
    with open("data/explanations_reinforcing.txt", "w") as w3:
        for explanation in data_df[data_df['effect_abstracted']==3]['explanation'].values:
            w3.write(explanation+'\n\n')
