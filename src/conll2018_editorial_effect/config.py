# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 0
# -----------------------------------------------------------------------
data_file_path = 'data/annotations/annotations_latest.csv'
# data_batch_json = '~/projects-private/emnlp2018/data/annotations/conll2018-news-editorial-quality_partial.json'
data_all_json = 'data/annotations/conll2018_data.json'

# Ids of annotators for each batch
batch1 = ['C09', 'L01', 'L03', 'C11', 'C03', 'L07']
batch2 = ['L08', 'C02', 'L14', 'L15', 'C12', 'C07']
batch3 = ['L05', 'L11', 'C14', 'L12', 'C10', 'C04']
batch4 = ['C15', 'L04', 'C06', 'L06', 'L09', 'C13']

# Available batches
batches = ['batch1', 'batch2', 'batch3', 'batch4']

batches_lst = [batch1, batch2, batch3, batch4]

# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 3
# -----------------------------------------------------------------------
personality_path = 'data/annotations/personality_traits.csv'

# -----------------------------------------------------------------------
# Source: conll18-analysis.ipynb, cell 4
# -----------------------------------------------------------------------
personality_dic = {'LOW': 1, 'AVERAGE': 2, 'HIGH': 3}

# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 2
# -----------------------------------------------------------------------
src = '../new-york-times-corpus-analysis/data/filtered_opinionated_content_only/'
path = src + '*.txt'
