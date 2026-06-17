from conll2018_editorial_effect.data.loader import (
    load_annotations,
    load_personality_traits,
    save_annotations_json,
)
from conll2018_editorial_effect.data.preprocessing import (
    preprocess,
    split_by_political_pole,
    add_political_pole_to_personality,
)
from conll2018_editorial_effect.analysis.agreement import (
    calculate_allbatches_agreement_old as calculate_allbatches_agreement,
    calculate_krippendorff,
    calculate_krippendorff_per_batch,
    get_editorialas_all_annotators_view,
    pairs_agrement_krip,
)
from conll2018_editorial_effect.analysis.quality import (
    get_majority_agreement,
    get_full_agreement,
    get_editorials_view_df,
    show_editorialsquality_results,
)
from conll2018_editorial_effect.analysis.statistics import (
    test_hypotheses,
    test_hypotheses_2,
)
from conll2018_editorial_effect.analysis.correlation import (
    show_correlation,
    show_correlation_tau,
    show_spearman_editorial_view,
    count_traits,
)
from conll2018_editorial_effect.utils.files import write_explanations


def section(title):
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)


# -----------------------------------------------------------------------
# 1. LOAD
# -----------------------------------------------------------------------
section("1. LOADING DATA")

print("  Loading annotation CSV...")
data_df = load_annotations()
print("  Loading personality traits CSV...")
data_personality_df = load_personality_traits()

assert len(data_df) > 0,             "annotations CSV is empty"
assert len(data_personality_df) > 0, "personality traits CSV is empty"
print(f"  [OK] {len(data_df)} raw annotations loaded")
print(f"  [OK] {len(data_personality_df)} personality records loaded")

# -----------------------------------------------------------------------
# 2. PREPROCESS
# -----------------------------------------------------------------------
section("2. PREPROCESSING")

print("  Adding columns (political pole, effect, batch, personality traits)...")
data_df = preprocess(data_df, data_personality_df)
print("  Splitting by political pole...")
liberals_df, conservatives_df = split_by_political_pole(data_df)
print("  Adding political pole to personality df...")
data_personality_df = add_political_pole_to_personality(data_personality_df)

# Total annotations after filtering dropped annotators
assert len(data_df) == 6000, f"expected 6000 annotations, got {len(data_df)}"

# Per ideology
assert len(liberals_df) == 3000,      f"expected 3000 liberal annotations, got {len(liberals_df)}"
assert len(conservatives_df) == 3000, f"expected 3000 conservative annotations, got {len(conservatives_df)}"
assert len(liberals_df) + len(conservatives_df) == len(data_df), "liberal + conservative counts don't add up to total"

# Unique articles and annotators
assert data_df['article_id'].nunique() == 1000, f"expected 1000 unique articles, got {data_df['article_id'].nunique()}"
assert data_df['annotator_id'].nunique() == 24, f"expected 24 annotators, got {data_df['annotator_id'].nunique()}"

# Batches
assert set(data_df['batch'].unique()) == {'batch1', 'batch2', 'batch3', 'batch4'}, \
    f"unexpected batch values: {data_df['batch'].unique()}"

# Political pole
assert set(data_df['political_pole'].unique()) == {'liberal', 'conservative'}, \
    f"unexpected political_pole values: {data_df['political_pole'].unique()}"

# Effect range
assert data_df['effect'].between(1, 5).all(), "effect values out of range [1, 5]"
assert set(data_df['effect_abstracted'].unique()) <= {1, 2, 3}, \
    f"unexpected effect_abstracted values: {data_df['effect_abstracted'].unique()}"
assert set(data_df['has_effect'].unique()) <= {0, 1}, \
    f"unexpected has_effect values: {data_df['has_effect'].unique()}"

# No duplicates
assert data_df.duplicated(['annotator_id', 'article_id']).sum() == 0, \
    "duplicate (annotator_id, article_id) pairs found after preprocessing"

# Expected columns (from conll18-analysis.ipynb, cell 8 output)
expected_cols = {
    'agreeableness', 'annotator_id', 'article_id', 'article_index', 'batch',
    'challenging', 'change', 'conscientiousness', 'date_created', 'effect',
    'effect_abstracted', 'explanation', 'extraversion', 'has_effect',
    'intensity', 'neuroticism', 'openness', 'political_pole',
    'political_typology', 'reinforce', 'reinforcing',
}
assert expected_cols.issubset(set(data_df.columns)), \
    f"missing columns: {expected_cols - set(data_df.columns)}"

print(f"  [OK] {len(data_df)} annotations — {len(liberals_df)} liberal, {len(conservatives_df)} conservative")
print(f"  [OK] {data_df['article_id'].nunique()} unique articles, {data_df['annotator_id'].nunique()} annotators, {data_df['batch'].nunique()} batches")

# -----------------------------------------------------------------------
# 3. SAVE JSON
# -----------------------------------------------------------------------
section("3. SAVING JSON")

print("  Saving all annotations to JSON...")
save_annotations_json(data_df)
print("  [OK] JSON saved")

# -----------------------------------------------------------------------
# 4. AGREEMENT — Fleiss / Cohen / Alpha
# -----------------------------------------------------------------------
section("4. INTER-RATER AGREEMENT — Fleiss / Cohen / Alpha")

columns_effect1to3 = ['annotator_id', 'article_id', 'effect_abstracted']
columns_has_effect = ['annotator_id', 'article_id', 'has_effect']

print("\n  -- Effect (1 to 3) --")
calculate_allbatches_agreement(conservatives_df, columns_effect1to3, 'EFFECT 1 TO 3 - CONSERVATIVES - OVERALL', 'overall')
calculate_allbatches_agreement(liberals_df,      columns_effect1to3, 'EFFECT 1 TO 3 - LIBERALS - OVERALL',      'overall')
calculate_allbatches_agreement(data_df,          columns_effect1to3, 'EFFECT 1 TO 3 - ALL - OVERALL',           'overall')

print("\n  -- Effect (1 to 3) — Pairs of 2 --")
calculate_allbatches_agreement(conservatives_df, columns_effect1to3, 'EFFECT 1 TO 3 - CONSERVATIVES - PAIRS OF 2', 'pairsOf2')
calculate_allbatches_agreement(liberals_df,      columns_effect1to3, 'EFFECT 1 TO 3 - LIBERALS - PAIRS OF 2',      'pairsOf2')
calculate_allbatches_agreement(data_df,          columns_effect1to3, 'EFFECT 1 TO 3 - ALL - PAIRS OF 2',           'pairsOf2')

print("\n  -- Has effect --")
calculate_allbatches_agreement(conservatives_df, columns_has_effect, 'has_effect - CONSERVATIVES - OVERALL', 'overall')
calculate_allbatches_agreement(liberals_df,      columns_has_effect, 'has_effect - LIBERALS - OVERALL',      'overall')
calculate_allbatches_agreement(data_df,          columns_has_effect, 'has_effect - ALL - OVERALL',           'overall')

# -----------------------------------------------------------------------
# 5. AGREEMENT — Krippendorff
# -----------------------------------------------------------------------
section("5. INTER-RATER AGREEMENT — Krippendorff's Alpha")

print("\n  -- Effect (1 to 5) --")
calculate_krippendorff(data_df, liberals_df, conservatives_df, effect_col='effect')
print("\n  -- Effect abstracted (1 to 3) --")
calculate_krippendorff(data_df, liberals_df, conservatives_df, effect_col='effect_abstracted')
print("\n  -- Per batch: effect (1 to 5) --")
calculate_krippendorff_per_batch(data_df, liberals_df, conservatives_df, effect_col='effect')
print("\n  -- Per batch: effect abstracted (1 to 3) --")
calculate_krippendorff_per_batch(data_df, liberals_df, conservatives_df, effect_col='effect_abstracted')

print("\n  -- Pairwise Krippendorff --")
d, _ = get_editorialas_all_annotators_view(data_df, 'effect_abstracted')
pairs_agrement_krip(d)

# -----------------------------------------------------------------------
# 6. AGREEMENT — Majority / Full
# -----------------------------------------------------------------------
section("6. INTER-RATER AGREEMENT — Majority & Full")

print("\n  -- Majority (effect 1 to 5) --")
print('  MAJORITY Agreement EFFECT 1 TO 5 - LIBE: ', str(get_majority_agreement(liberals_df)))
print('  MAJORITY Agreement EFFECT 1 TO 5 - CONS: ', str(get_majority_agreement(conservatives_df)))
print('  MAJORITY Agreement EFFECT 1 TO 5 - ALL : ', str(get_majority_agreement(data_df)))

print("\n  -- Full (effect 1 to 5) --")
print('  FULL Agreement EFFECT 1 TO 5 - LIBE: ', str(get_full_agreement(liberals_df)))
print('  FULL Agreement EFFECT 1 TO 5 - CONS: ', str(get_full_agreement(conservatives_df)))
print('  FULL Agreement EFFECT 1 TO 5 - ALL : ', str(get_full_agreement(data_df)))

print("\n  -- Full (effect 1 to 3) --")
print('  FULL Agreement EFFECT 1 TO 3 - LIBE: ', str(get_full_agreement(liberals_df, columns=['article_id', 'effect_abstracted'])))
print('  FULL Agreement EFFECT 1 TO 3 - CONS: ', str(get_full_agreement(conservatives_df, columns=['article_id', 'effect_abstracted'])))
print('  FULL Agreement EFFECT 1 TO 3 - ALL : ', str(get_full_agreement(data_df, columns=['article_id', 'effect_abstracted'])))

# -----------------------------------------------------------------------
# 7. QUALITY — Editorial majority votes
# -----------------------------------------------------------------------
section("7. EDITORIAL QUALITY — Majority Votes per Article")

print("\n  -- Abstract effect (1 to 3) --")
show_editorialsquality_results(data_df, for_abstract_effect=True)
print("\n  -- Effect (1 to 5) --")
show_editorialsquality_results(data_df, for_abstract_effect=False)

editorials_view_df = get_editorials_view_df(data_df)
assert len(editorials_view_df) == 1000, \
    f"expected 1000 rows in editorial view, got {len(editorials_view_df)}"
print(f"  [OK] Editorial majority view: {len(editorials_view_df)} articles")

# -----------------------------------------------------------------------
# 8. HYPOTHESIS TESTING
# -----------------------------------------------------------------------
section("8. HYPOTHESIS TESTING")

print("\n  -- Mann-Whitney: effect (1 to 3) --")
test_hypotheses(data_df)
print("\n  -- Mann-Whitney: effect (1 to 5) --")
test_hypotheses(data_df, is1To5=True)
print("\n  -- Wilcoxon: reinforcing --")
test_hypotheses_2(data_df)

# -----------------------------------------------------------------------
# 9. CORRELATION — Editorial view (Spearman)
# -----------------------------------------------------------------------
section("9. CORRELATION — Liberal vs Conservative Editorial View (Spearman)")

show_spearman_editorial_view(editorials_view_df)

# -----------------------------------------------------------------------
# 10. CORRELATION — Personality traits (Spearman + Kendall tau)
# -----------------------------------------------------------------------
section("10. CORRELATION — Personality Traits")

print("\n  -- Spearman: effect abstracted --")
show_correlation(liberals_df,      'effect_abstracted LIBERALS')
show_correlation(conservatives_df, 'effect_abstracted CONSERVATIVES')
show_correlation(data_df,          'effect_abstracted OVERALL')

print("\n  -- Spearman: challenging --")
show_correlation(liberals_df,      'challenging LIBERALS',      col='challenging')
show_correlation(conservatives_df, 'challenging CONSERVATIVES', col='challenging')
show_correlation(data_df,          'challenging OVERALL',       col='challenging')

print("\n  -- Spearman: reinforcing --")
show_correlation(liberals_df,      'reinforcing LIBERALS',      col='reinforcing')
show_correlation(conservatives_df, 'reinforcing CONSERVATIVES', col='reinforcing')
show_correlation(data_df,          'reinforcing OVERALL',       col='reinforcing')

print("\n  -- Spearman: has_effect --")
show_correlation(liberals_df,      'has_effect LIBERALS',      col='has_effect')
show_correlation(conservatives_df, 'has_effect CONSERVATIVES', col='has_effect')
show_correlation(data_df,          'has_effect OVERALL',       col='has_effect')

print("\n  -- Kendall tau: has_effect --")
show_correlation_tau(liberals_df,      'has_effect LIBERALS',      col='has_effect')
show_correlation_tau(conservatives_df, 'has_effect CONSERVATIVES', col='has_effect')
show_correlation_tau(data_df,          'has_effect OVERALL',       col='has_effect')

# -----------------------------------------------------------------------
# 11. PERSONALITY TRAITS — Count distribution
# -----------------------------------------------------------------------
section("11. PERSONALITY TRAITS — Distribution")

assert data_personality_df['political_pole'].nunique() == 2, \
    f"expected 2 political poles in personality df, got {data_personality_df['political_pole'].nunique()}"
print(f"  [OK] {len(data_personality_df)} annotators across 2 political poles")

print('\n  ########### LIBERALS ############')
count_traits(liberals_df)
print('\n  ########### CONSERVATIVES ############')
count_traits(conservatives_df)
print('\n  ########### OVERALL ############')
count_traits(data_df)
count_traits(data_personality_df)

# -----------------------------------------------------------------------
# 12. WRITE EXPLANATIONS
# -----------------------------------------------------------------------
section("12. WRITING EXPLANATION FILES")

print("  Writing explanations by effect category...")
write_explanations(data_df)
print("  [OK] Wrote: data/explanations_challenging.txt")
print("  [OK] Wrote: data/explanations_noeffect.txt")
print("  [OK] Wrote: data/explanations_reinforcing.txt")

section("DONE")
