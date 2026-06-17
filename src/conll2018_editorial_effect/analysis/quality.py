import pandas as pd


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 22
# Change: none
# -----------------------------------------------------------------------
def get_majority_agreement(df, columns = ['article_id', 'effect']):
    df_editorial_view = df[columns]
    majority = 0
    total = 0
    for g in df_editorial_view.groupby(columns[0]):
        # counting the number of all effect
        grouped = g[1].groupby([columns[1]]).agg(['count'])
        majority = majority + grouped[(columns[0], 'count')].max()
        total = total + grouped[(columns[0], 'count')].sum()
    return majority/total

def get_majority_agreement_effectnoeffect(df, columns = ['article_id', 'has_effect']):
    df_editorial_view = df[columns]
    majority = 0
    total = 0
    for g in df_editorial_view.groupby(columns[0]):
        # counting the number of all effect
        grouped = g[1].groupby(['has_effect']).agg(['count'])
        majority = majority + grouped[('has_effect', 'count')].max()
        total = total + grouped[('has_effect', 'count')].sum()
    return majority/total

def get_full_agreement_effectnoeffect(df, columns = ['article_id', 'has_effect']):
    df_editorial_view = df[columns]
    full = 0
    counter = 0
    for g in df_editorial_view.groupby([columns[0]]):
        # counting the number of all effect
        counter = counter +1
        grouped = g[1].groupby(['has_effect']).agg(['count'])
        majority =  grouped[(columns[0], 'count')].max()
        total =  grouped[(columns[0], 'count')].sum()
        if majority == total :
            full =  full + 1
    return full/counter

def get_full_agreement(df, columns = ['article_id', 'effect']):
    df_editorial_view = df[columns]
    full = 0
    counter = 0
    for g in df_editorial_view.groupby([columns[0]]):
        # counting the number of all effect
        counter = counter +1
        grouped = g[1].groupby([columns[1]]).agg(['count'])
        majority =  grouped[(columns[0], 'count')].max()
        total =  grouped[(columns[0], 'count')].sum()
        if majority == total :
            full =  full + 1
    return full/counter


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 27
# Change: data_df passed as argument instead of global variable
# -----------------------------------------------------------------------
def get_editorials_view_df(data_df, columns = ['article_id', 'effect_abstracted', 'political_pole', 'change', 'reinforce'], no_effect_val = 2):
    df_editorial_view = data_df[columns]
    editorials_majority_votes_list = []
    no_majority = 0
    for article_id, g in df_editorial_view.groupby('article_id'):
        # counting the number of all effect
        article_maj_vote_dic = {}
        article_maj_vote_dic = {'id': article_id}
        # Change: groupby('political_pole') not groupby(['political_pole']) — list form
        #         produces tuple keys ('conservative',) instead of string 'conservative'
        for political_pole, subgroup in g.groupby('political_pole'):
            vals = subgroup[columns[1]].values
            colname_start = 'l'
            if political_pole == 'conservative': colname_start = 'c'
            article_maj_vote_dic[colname_start + '1'] = vals[0]
            article_maj_vote_dic[colname_start + '2'] = vals[1]
            article_maj_vote_dic[colname_start + '3'] = vals[2]
            group_effect = subgroup.groupby(columns[1]).agg(['count'])
            # Change: argmax() -> idxmax() for pandas >= 1.0
            major_effect = group_effect[('article_id', 'count')].idxmax()
            max_votes = group_effect[('article_id', 'count')].max()
            has_effect = 1
            if max_votes <= 1:
                no_majority = no_majority +1
                #print('No majority for article ', g[0], ', pole:', subgroup[0])
                major_effect = 0
            if major_effect == 0 :
                has_effect = -1
            if  major_effect == no_effect_val:
                has_effect = 0

            if 'change' in columns:
                group_change = subgroup.groupby('change').agg(['count'])
                major_change = 0
                if not group_change.empty:
                    major_change = group_change[('article_id', 'count')].argmax()
                    max_change = group_change[('article_id', 'count')].max()
                    if max_change <= 1:
                        major_change = 0
                article_maj_vote_dic[colname_start+'_change'] = 1 if (major_change == 'YES') else 0
            if 'reinforce' in columns:
                group_empower = subgroup.groupby('reinforce').agg(['count'])
                major_empower = 0
                if not group_empower.empty:
                    major_empower = group_empower[('article_id', 'count')].argmax()
                    max_empower = group_empower[('article_id', 'count')].max()
                    if max_empower <= 1:
                        major_empower = 0
                    article_maj_vote_dic[colname_start+'_empower'] = 1 if (major_empower == 'YES') else 0

            article_maj_vote_dic[colname_start+'_haseffect'] = has_effect
            article_maj_vote_dic[colname_start+'_noeffect'] = 1 if (has_effect == 0) else 0
            article_maj_vote_dic[colname_start+'_challenging'] = 1 if (major_effect == 1) else 0
            article_maj_vote_dic[colname_start+'_reinforcing'] = 1 if (major_effect == 3) else 0
            article_maj_vote_dic[political_pole] = major_effect

        editorials_majority_votes_list.append(article_maj_vote_dic)

    print('Number of articles not having majority:', no_majority)
    # Change: from_dict -> pd.DataFrame; from_dict expects a dict, not a list of dicts
    return pd.DataFrame(editorials_majority_votes_list)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 28
# Change: data_df passed as argument instead of global variable
# -----------------------------------------------------------------------
def show_editorialsquality_results(data_df, for_abstract_effect = True):
    editorials_maj_df = get_editorials_view_df(data_df)
    if not for_abstract_effect:
        editorials_maj_df = get_editorials_view_df(data_df, ['article_id', 'effect', 'political_pole'])
    total = len(editorials_maj_df)
    challenging_challenging = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 1) & (editorials_maj_df['liberal'] == 1) ])
    reinforcing_reinforcing = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 3) & (editorials_maj_df['liberal'] == 3) ])
    noeffect_noeffect = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 2) & (editorials_maj_df['liberal'] == 2) ])

    # CHALLENGING REINFORCING
    cons_challenging_lib_reinforcing = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 1) & (editorials_maj_df['liberal'] == 3) ])
    lib_challenging_cons_reinforcing = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 3) & (editorials_maj_df['liberal'] == 1) ])
    challenging_reinforcing = cons_challenging_lib_reinforcing + lib_challenging_cons_reinforcing

    # CHALLENGING NO EFFECT
    cons_challenging_lib_noeffect = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 1) & (editorials_maj_df['liberal'] == 2) ])
    lib_challenging_cons_noeffect = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 2) & (editorials_maj_df['liberal'] == 1) ])
    challenging_noeffect = cons_challenging_lib_noeffect + lib_challenging_cons_noeffect

    # REINFORCING NO EFFECT
    cons_reinforcing_lib_noeffect = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 3) & (editorials_maj_df['liberal'] == 2) ])
    lib_reinforcing_cons_noeffect = len(editorials_maj_df[ (editorials_maj_df['conservative'] == 2) & (editorials_maj_df['liberal'] == 3) ])
    reinforcing_noeffect = cons_reinforcing_lib_noeffect + lib_reinforcing_cons_noeffect

    print('CHALLENGING-REINFORCING:', challenging_reinforcing , '(' + str(((challenging_reinforcing/total)*100)) +'%)')
    print('liberal-cons:', lib_challenging_cons_reinforcing)
    print('cons-liberal:', cons_challenging_lib_reinforcing)
    print()
    print('CHALLENGING-CHALLENGING:', challenging_challenging, '(' + str(((challenging_challenging/total)*100)) +'%)')
    print()
    print('REINFORCING-REINFORCING:', reinforcing_reinforcing, '(' + str(((reinforcing_reinforcing/total)*100)) +'%)')
    print()
    print('CHALLENGING-NO EFFECT  :', challenging_noeffect, '(' + str(((challenging_noeffect/total)*100)) +'%)')
    print('liberal-cons:', lib_challenging_cons_noeffect)
    print('cons-liberal:', cons_challenging_lib_noeffect)
    print()
    print('REINFORCING-NO EFFECT  :', reinforcing_noeffect, '(' + str(((reinforcing_noeffect/total)*100)) +'%)')
    print('liberal-cons:', lib_reinforcing_cons_noeffect)
    print('cons-liberal:', cons_reinforcing_lib_noeffect)
    print()
    print('NO EFFECT-NO EFFECT    :', noeffect_noeffect, '(' + str(((noeffect_noeffect/total)*100)) +'%)')
    print()
    print()
    print()
    # Change: guarded by for_abstract_effect — c_change/l_change/c_empower/l_empower
    #         are only built when the default columns (including 'change','reinforce') are used
    if for_abstract_effect:
        print(len(editorials_maj_df[editorials_maj_df['c_change'] == 'YES']))
        print(len(editorials_maj_df[editorials_maj_df['l_change'] == 'YES']))
        print(len(editorials_maj_df[editorials_maj_df['l_empower'] == 'YES']))
        print(len(editorials_maj_df[editorials_maj_df['c_empower'] == 'YES']))
