import itertools

import krippendorff
import numpy as np
import pandas as pd
from nltk import agreement
from nltk.metrics import binary_distance, interval_distance, masi_distance

from conll2018_editorial_effect.config import batches, batches_lst


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 16
# Change: none
# -----------------------------------------------------------------------
test_name_fleiss = 'fleiss'
test_name_cohen = 'cohen'
test_name_alpha = 'alpha'

def preformat_and_calculate_agreement(df, test_name): #is_cohen = False):
    d = [ tuple(k.values()) for k in  df.T.to_dict().values()]

    # each is ('L07', '1638699.txt', 4)

    # for krip alpha that supports ordinal data, we need to used another library and it needs
    # Each data in list of array for each annotator
    return calculate_agreement(d, test_name)

def calculate_agreement(formattedData, test_name, kripp_data = None):
    rating_task = agreement.AnnotationTask(data=formattedData)#, distance=interval_distance)
    r = 0
    try:
        if test_name == test_name_cohen:
            r = rating_task.kappa()
        elif test_name == test_name_fleiss:
            r= rating_task.multi_kappa()
        elif test_name == test_name_alpha:
            r = rating_task.alpha()
        else:
            print('This test is not supported')
    except Exception as e:
        print("Exception." + str(formattedData))
        print(e)
        r = float('NaN')
    return r


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 17
# Change: none
# -----------------------------------------------------------------------
def calculate_agreement_raters_combination(d, rater_id = 'annotator_id', raters_pairs=None, agreement_test= test_name_cohen ):
    result = {}
    if raters_pairs == None:
        #print('Raters pair is none and we are are creating a list of 2 raters')
        raters_pairs =[]
        for b in batches_lst :
            inter_set = set(b).intersection(set(d[rater_id].unique()))
            raters_pairs.extend(list(itertools.combinations(list(inter_set), 2)))

    dfs = [d[d[rater_id].isin(x)] for x in raters_pairs]

    #Here do for each batch pairs of 2
    for raters_pairs_df in dfs:
        result[str(raters_pairs_df[rater_id].unique())] = preformat_and_calculate_agreement(raters_pairs_df, agreement_test)
    return  np.average(list(result.values()))


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 18
# Change: none
# -----------------------------------------------------------------------
def calculate_allbatches_agreement_old(original_df, columns_to_keep, description, agreement_style):
    agreement_result = {}
    agreement_result_alpha = {}
    for batch in batches:
        df = original_df[original_df['batch'] == batch]
        df = df[columns_to_keep]

        if agreement_style == 'overall':
            agreement_result[batch] = preformat_and_calculate_agreement(df, test_name_fleiss)
            agreement_result_alpha[batch] = preformat_and_calculate_agreement(df, test_name_alpha)
        elif agreement_style == 'pairsOf2':
            agreement_result[batch] = calculate_agreement_raters_combination(df)
            agreement_result_alpha[batch] = calculate_agreement_raters_combination(df, agreement_test =test_name_alpha)
    r = np.average(list(agreement_result.values()))
    a = np.average(list(agreement_result_alpha.values()))

    print(description)
    print('----> Fleiss/Cohen',  str(r))
    print('---->        alpha',  str(a))
    return  r, a


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 19
# Change: initialized r and a to float('NaN') to avoid possibly-unbound error
#         if agreement_style doesn't match 'overall' or 'pairsOf2'
# -----------------------------------------------------------------------
def calculate_allbatches_agreement(original_df, columns_to_keep, description, agreement_style):
    df = original_df[columns_to_keep]
    r = float('NaN')
    a = float('NaN')

    if agreement_style == 'overall':
        r = preformat_and_calculate_agreement(df, test_name_fleiss)
        a = preformat_and_calculate_agreement(df, test_name_alpha)
    elif agreement_style == 'pairsOf2':
        r = calculate_agreement_raters_combination(df)
        a = calculate_agreement_raters_combination(df, agreement_test =test_name_alpha)
    print(description)
    print('----> Fleiss/Cohen',  str(r))
    print('---->        alpha',  str(a))
    return  r, a


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 51
# Change: none
# -----------------------------------------------------------------------
def get_editorialas_all_annotators_view(d, effect_col, dropna = True):
    l = []
    rows_articles_ids = d['article_id'].unique()
    cols_all_annotators_list =   list(d['annotator_id'].unique())   #(np.array(batches_lst)).flatten()
    cols_all_annotators_list.append('batch')
    df = pd.DataFrame(index=rows_articles_ids, columns= cols_all_annotators_list , data= np.nan)

    for i, r in d.iterrows() :
        article_id = r['article_id']
        annotator = r['annotator_id']
        effect = r[effect_col]
        df.loc[article_id][annotator] = int(effect)

        df.loc[article_id]['batch'] = r['batch']
 #   if dropna:
 #       df.dropna(inplace = True)
    return df , df.T.values


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 53
# Change: wrapped in a function; data_df, liberals_df, conservatives_df
#         passed as arguments
# -----------------------------------------------------------------------
def calculate_krippendorff(data_df, liberals_df, conservatives_df, effect_col='effect'):
    _, kripp_data = get_editorialas_all_annotators_view(data_df, effect_col, dropna= False)
    _, kripp_data_liberals = get_editorialas_all_annotators_view(liberals_df, effect_col, dropna= False)
    _, kripp_data_conservatives = get_editorialas_all_annotators_view(conservatives_df, effect_col, dropna= False)

    print("Krippendorff's alpha for ordinal metric - ALL: ", krippendorff.alpha(reliability_data=kripp_data,
                                                                      level_of_measurement='ordinal'))
    print("Krippendorff's alpha for ordinal metric - LIBERALS: ", krippendorff.alpha(reliability_data=kripp_data_liberals,
                                                                      level_of_measurement='ordinal'))
    print("Krippendorff's alpha for ordinal metric - CONSERVATIVES: ", krippendorff.alpha(reliability_data=kripp_data_conservatives,
                                                                      level_of_measurement='ordinal'))


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 54
# Change: wrapped in a function; data_df, liberals_df, conservatives_df
#         passed as arguments
# -----------------------------------------------------------------------
def calculate_krippendorff_per_batch(data_df, liberals_df, conservatives_df, effect_col='effect'):
    for b in batches:
        _, kripp_data = get_editorialas_all_annotators_view(data_df[data_df['batch'] == b], effect_col)
        _, kripp_data_liberals = get_editorialas_all_annotators_view(liberals_df[liberals_df['batch'] == b], effect_col)
        _, kripp_data_conservatives = get_editorialas_all_annotators_view(conservatives_df[conservatives_df['batch'] == b], effect_col)
        print(b+" - Krippendorff's alpha for ordinal metric - ALL: ", krippendorff.alpha(reliability_data=kripp_data,
                                                                      level_of_measurement='ordinal'))
        print(b+" - Krippendorff's alpha for ordinal metric - LIBERALS: ", krippendorff.alpha(reliability_data=kripp_data_liberals,
                                                                          level_of_measurement='ordinal'))
        print(b+" - Krippendorff's alpha for ordinal metric - CONSERVATIVES: ", krippendorff.alpha(reliability_data=kripp_data_conservatives,
                                                                          level_of_measurement='ordinal'))
        print()
        print()
        print()


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 57
# Change: raters_pairs moved from global to local variable inside function
# -----------------------------------------------------------------------
def pairs_agrement_krip(d):
    raters_pairs =[]
    r = {}
    r_perbatch = {}
    counter = 0
    for b in batches_lst :
        batch_alphas_lst = []
        inter_set = set(b).intersection(set(d.columns))
        raters_pairs.extend(list(itertools.combinations(list(inter_set), 2)))
        print (d.columns)

        dfs = [ d[list(x) ] for x in raters_pairs]
        for df in dfs :
            key = tuple(df.columns)
            df.dropna(inplace=True)
            alpha =  krippendorff.alpha(reliability_data = df.T.values, level_of_measurement='ordinal')
            r[key] = alpha
            batch_alphas_lst.append(alpha)

        r_perbatch[batches[counter]] = batch_alphas_lst
        counter = counter +1

    scores = {}
    # Overall score
    scores['overall'] =  np.average(list(r.values()))
    # perbatch score
    for k, v in r_perbatch.items():
        avg =  np.average(v)
        scores[k] = avg
    return scores


# -----------------------------------------------------------------------
# Source: inter-rater-agreement.ipynb, cell 1
# Change: none
# -----------------------------------------------------------------------
def fleiss(d, desc):
    ratingtask = agreement.AnnotationTask(data=d)
    #print(desc, " - fleiss " + str(ratingtask.multi_kappa()))
    print(desc, " - alpha " + str(ratingtask.alpha()))


# -----------------------------------------------------------------------
# Source: inter-rater-agreement.ipynb, cell 10
# Change: none
# -----------------------------------------------------------------------
def calculate_fleiss(df, is_cohen = False):
    d = [ list(k.values()) for k in  df.T.to_dict().values()]
    #  if isinstance( d[0][2], list):
    #      d = flatten_pro_list(d)
    return fleiss_kappa(d, is_cohen)

def fleiss_kappa(formattedData, is_cohen = False):
    rating_task = agreement.AnnotationTask(data=formattedData)
    r = 0
    a = 0
    try:
        if is_cohen:
            r = rating_task.kappa()
        else:
            r= rating_task.multi_kappa()
        a = rating_task.alpha()
    except Exception as e:
        print("Exception." + str(formattedData))
        print(e)
        r = float('NaN')
    return a


# -----------------------------------------------------------------------
# Source: inter-rater-agreement.ipynb, cell 11
# Change: none
# -----------------------------------------------------------------------
def calculate_agreement_raters_combination_pilot(d, rater_id = 'annotator-id', raters_pairs=None ):
    result = {}
    if raters_pairs == None:
        print('SHOULD NO GO IN')
        raters_pairs = list(itertools.combinations(d[rater_id].unique(), 2))
    dfs = [d[d[rater_id].isin(x)] for x in raters_pairs]
    for raters_pairs_df in dfs:
        result[str(raters_pairs_df[rater_id].unique())] = calculate_fleiss(raters_pairs_df, True)
    return result, str(np.average(list(result.values())))
