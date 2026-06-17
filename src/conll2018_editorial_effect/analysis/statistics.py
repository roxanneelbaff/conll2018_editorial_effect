import numpy as np
import scipy.stats as stats
from scipy.stats import shapiro

from conll2018_editorial_effect.analysis.quality import get_editorials_view_df


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 39
# Change: none
# -----------------------------------------------------------------------
def isNormallyDistributed(l):
    return (shapiro(l)[1] >= 0.05)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 33
# Change: data_df passed as argument instead of relying on global variable
#         via get_editorials_view_df
# -----------------------------------------------------------------------
def test_hypotheses(data_df, is1To5 = False):
    # Hypothesis: The effect is the same for Conservative and liberal
    ## Ordinal data, 1 DV and 2IV -->  Wilcoxon-Mann Whitney test (Non paramtric test. no need to check normaly distributed)
    editorials_maj_df = get_editorials_view_df(data_df)
    if is1To5 :
        editorials_maj_df = get_editorials_view_df(data_df, ['article_id', 'effect', 'political_pole'])
    #Wilcoxon-Mann Whitney test
    print('############# liberal conservatives ###########')
    print('conservatives data - Normally distributed:', isNormallyDistributed(editorials_maj_df['conservative']))
    print('liberals data - Normally distributed:', isNormallyDistributed(editorials_maj_df['liberal']))
    ttest_stat, p_value = stats.mannwhitneyu(editorials_maj_df['conservative'], editorials_maj_df['liberal'])
    p_value= p_value/2
    print('H: There is no significance difference in annotating editorials effect between conservatives and liberals: ',ttest_stat, ' p-value:',   p_value)

    print('############# conservatives ###########')
    #Kruskal Wallis
    # Hypothesis: The effect is the same for all conservatives - ?SHOULD BE CALCULATED IN EACH BATCH !
    print('c1 data - Normally distributed:', isNormallyDistributed(editorials_maj_df['c1']))
    print('c2 data - Normally distributed:', isNormallyDistributed(editorials_maj_df['c2']))
    print('c3 data - Normally distributed:', isNormallyDistributed(editorials_maj_df['c3']))
    stat_cons, p_value_cons = stats.kruskal(editorials_maj_df['c1'], editorials_maj_df['c2'], editorials_maj_df['c3'])
    print('H: There is no significance difference in annotating editorials effect between conservatives: ',stat_cons, ' p-value',  (p_value_cons/2))

    print('############# liberal ###########')
    # Change: stat_lib and p_value_lib were referenced but never computed in the original notebook.
    #         Added the missing Kruskal-Wallis call mirroring the conservatives block above.
    print('l1 data - Normally distributed:', isNormallyDistributed(editorials_maj_df['l1']))
    print('l2 data - Normally distributed:', isNormallyDistributed(editorials_maj_df['l2']))
    print('l3 data - Normally distributed:', isNormallyDistributed(editorials_maj_df['l3']))
    stat_lib, p_value_lib = stats.kruskal(editorials_maj_df['l1'], editorials_maj_df['l2'], editorials_maj_df['l3'])
    print('H: There is no significance difference in annotating editorials effect between liberals: ',stat_lib, ' p-value',  p_value_lib/2)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 35
# Change: data_df passed as argument instead of relying on global variable
#         via get_editorials_view_df
# -----------------------------------------------------------------------
def test_hypotheses_2(data_df):
    # Hypothesis: The effect is the same for Conservative and liberal
    ## Ordinal data, 1 DV and 2IV -->  Wilcoxon-Mann Whitney test (Non paramtric test. no need to check normaly distributed)
    editorials_maj_df = get_editorials_view_df(data_df)
    editorials_maj_df = get_editorials_view_df(data_df, ['article_id', 'effect_abstracted', 'political_pole'])
    #Wilcoxon-Mann Whitney test
    print('############# liberal conservatives ###########')
    ttest_stat, p_value = stats.wilcoxon(editorials_maj_df['c_reinforcing'], editorials_maj_df['l_reinforcing'])
    p_value= p_value/2
    print('H: There is no significance difference in annotating editorials effect between conservatives and liberals: ',ttest_stat, ' p-value:',   p_value)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 44
# Change: wrapped in a function; lieral_lst and cons_lst passed as arguments
# -----------------------------------------------------------------------
def test_chi2_contingency(liberal_lst, cons_lst):
    obs = np.array([liberal_lst, cons_lst])
    # This makes total sense. it tells us if the two variables, typology and effect choice, are related

    # If the proportions of individuals in the different columns vary significantly between rows (or vice versa),
    #   it is said that there is a contingency between the two variables.
    # In other words, the two variables are not independent. If there is no contingency,
    # it is said that the two variables are independent.

    g, p, dof, expected = stats.chi2_contingency(obs)
    print(p)
    return g, p, dof, expected


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 46
# Change: wrapped in a function; obs passed as argument
# -----------------------------------------------------------------------
def test_chisquare(liberal_lst, cons_lst):
    obs = np.array([liberal_lst, cons_lst])
    return stats.chisquare(obs)
    # same as stats.power_divergence(obs)


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cells 76-81
# Change: wrapped in a function; values passed as arguments;
#         binom_test -> binomtest for scipy >= 1.9 (returns BinomTestResult)
# -----------------------------------------------------------------------
def test_binomial(k, n, p, alternative):
    return scipy.stats.binomtest(k, n=n, p=p, alternative=alternative)
