import scipy.stats


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 68
# Change: wrapped in a function; td passed as argument
# -----------------------------------------------------------------------
def spearman(td):
    rho, p_value = scipy.stats.spearmanr(td)
    print(scipy.stats.spearmanr(td))
    return rho, p_value


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cells 71 + 72
# Change: wrapped in a function; d passed as argument
# -----------------------------------------------------------------------
def show_spearman_editorial_view(d):
    print('lib challenging VS. cons. challending', scipy.stats.spearmanr(d['l_challenging'].values, d['c_challenging'].values))
    print('lib challenging VS. cons. reinf',       scipy.stats.spearmanr(d['l_challenging'].values, d['c_reinforcing'].values))
    print('lib rein VS. cons. chall',              scipy.stats.spearmanr(d['l_reinforcing'].values, d['c_challenging'].values))
    print('lib rein VS. cons. reinf',              scipy.stats.spearmanr(d['l_reinforcing'].values, d['c_reinforcing'].values))

    print('lib VS. cons.',                         scipy.stats.spearmanr(d['liberal'].values, d['conservative'].values))
    print('l_empower VS. c_empower.',              scipy.stats.spearmanr(d['l_empower'].values, d['c_empower'].values))
    #print('l_change VS. c_change.',               scipy.stats.spearmanr(d['l_change'].values, d['c_change'].values))
    #print('l_change VS. c_change.',               scipy.stats.spearmanr(d['l_change'].values, d['c_change'].values))
    print('l_haseffect VS. c_haseffect.',          scipy.stats.spearmanr(d['l_haseffect'].values, d['c_haseffect'].values))
    print('l_challenging VS. c_haseffect.',        scipy.stats.spearmanr(d['l_challenging'].values, d['c_haseffect'].values))
    print('l_haseffect VS. c_challenging.',        scipy.stats.spearmanr(d['l_haseffect'].values, d['c_challenging'].values))
    print('l_haseffect VS. c_reinforcing.',        scipy.stats.spearmanr(d['l_haseffect'].values, d['c_reinforcing'].values))


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 88
# Change: none (data_df already a parameter in original)
# -----------------------------------------------------------------------
def show_correlation_tau(data_df, desc, col = 'has_effect'):
    print('--------------------- ', desc, ' ---------------------')
    print()
    print('agreeableness VS. ', col, ' :', scipy.stats.kendalltau(data_df['agreeableness'].values, data_df[col].values))
    print('conscientiousness VS. ', col, ' :', scipy.stats.kendalltau(data_df['conscientiousness'].values, data_df[col].values))
    print('extraversion VS. ', col, ' :', scipy.stats.kendalltau(data_df['extraversion'].values, data_df[col].values))
    print('neuroticism VS. ', col, ' :', scipy.stats.kendalltau(data_df['neuroticism'].values, data_df[col].values))
    print('openness VS. ', col, ' :', scipy.stats.kendalltau(data_df['openness'].values, data_df[col].values))
    print('----------------------------------------------------------------------------------')


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 89
# Change: none (data_df already a parameter in original)
# -----------------------------------------------------------------------
def show_correlation(data_df, desc, col = 'effect_abstracted'):
    print('--------------------- ', desc, ' ---------------------')
    print()
    print('agreeableness VS. ', col, ' :', scipy.stats.spearmanr(data_df['agreeableness'].values, data_df[col].values))
    print('conscientiousness VS. ', col, ' :', scipy.stats.spearmanr(data_df['conscientiousness'].values, data_df[col].values))
    print('extraversion VS. ', col, ' :', scipy.stats.spearmanr(data_df['extraversion'].values, data_df[col].values))
    print('neuroticism VS. ', col, ' :', scipy.stats.spearmanr(data_df['neuroticism'].values, data_df[col].values))
    print('openness VS. ', col, ' :', scipy.stats.spearmanr(data_df['openness'].values, data_df[col].values))
    print('----------------------------------------------------------------------------------')


# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 96
# Change: none (d already a parameter in original)
# -----------------------------------------------------------------------
def count_traits(d):
    print('agreeableness:', d['agreeableness'].value_counts())
    print('conscientiousness:', d['conscientiousness'].value_counts())
    print('extraversion:', d['extraversion'].value_counts())
    print('neuroticism:', d['neuroticism'].value_counts())
    print('openness:', d['openness'].value_counts())
    print('##################################')
