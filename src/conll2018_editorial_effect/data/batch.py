# -----------------------------------------------------------------------
# ARCHIVE ONLY — requires the NYT corpus (licensed, not distributed).
# The batch data produced by this module is already included in data/batch{n}/.
# Users who do not hold the NYT corpus license can use those directly.
# -----------------------------------------------------------------------

import glob
from shutil import copy2

import matplotlib.pyplot as plt
import numpy as np

from conll2018_editorial_effect.utils.files import get_filename
from conll2018_editorial_effect.config import src, path


# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 5
# Change: wrapped in a function; src/path taken from config
# -----------------------------------------------------------------------
def compute_article_length_stats():
    mini = -1
    maxi = -1
    avg = 0
    c = 0
    for item in glob.glob(path):
        c = c + 1
        with open(item, 'r') as myfile:
            data = myfile.read()
            l = len(data.split(' '))
            avg = avg + l
            if (l < mini or mini == -1): mini = l
            if (l > maxi): maxi = l
    print(mini)
    print(maxi)
    avg = avg / c
    print(avg)

    #chars
    #547
    #11133
    #2697.287949921753

    #words
    #117
    #2066
    #491.67605633802816


# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 6
# Change: wrapped in a function; avg and length bounds moved to arguments
# -----------------------------------------------------------------------
def filter_articles_by_length(avg=492, min_len=450, max_len=650):
    articles_below_avg = 0
    articles_above_avg = 0
    articles_between = 0

    article_lengths = []
    keep_files = []
    for item in glob.glob(path):
        with open(item, 'r') as myfile:
            data = myfile.read()
            l = len(data.split(' '))
            article_lengths.append(l)
            if l < avg: articles_below_avg = articles_below_avg+1
            else: articles_above_avg = articles_above_avg+1

            if (l > min_len and l<=max_len):
                articles_between = articles_between+1
                keep_files.append(item)

    return keep_files, article_lengths, articles_below_avg, articles_above_avg, articles_between


# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cells 15 + 16
# Change: wrapped in a function; keep_files passed as argument
# -----------------------------------------------------------------------
def create_batches(keep_files, n_batches=5, batch_size=200):
    file_name_array = [get_filename(item) for item in keep_files]
    batches_array = np.random.choice(file_name_array, size=(n_batches, batch_size), replace=False)

    #test that there are no duplicates
    for i in range(n_batches):
        for j in range(n_batches):
            if (i != j):
                print(any(x in set(batches_array[i]) for x in batches_array[j]))

    for i in range(n_batches):
        # New batch
        dst = 'data/batch' + (str(i + 1)) + '/'
        batch = batches_array[i]

        for f in batch:
            copy2((src + f + '.txt'), dst)

    return batches_array, file_name_array


# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 17
# Change: wrapped in a function; batches_array and file_name_array passed as arguments
# -----------------------------------------------------------------------
def create_pilot_and_backup(file_name_array, batches_array):
    backup = [item for item in file_name_array if (not any(item in taken for taken in batches_array))]
    pilot = np.random.choice(backup, 5, replace=False)

    for f in backup:
        if f not in pilot:
            copy2((src + f + '.txt'), 'data/backup')

    for f in pilot:
        copy2((src + f + '.txt'), 'data/pilot')


# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 18
# Change: wrapped in a function
# Note: cell 19 (copy to /home/cifo3206/...) is a one-off deployment step,
#       not included
# -----------------------------------------------------------------------
def redistribute_batch5(n_batches=4, batch_size=50):
    files_in_batch5 = glob.glob('data/batch5/*.txt')
    print(len(files_in_batch5))
    file_names_inb5 = [get_filename(f) for f in files_in_batch5]
    batches5_array = np.random.choice(file_names_inb5, size=(n_batches, batch_size), replace=False)
    for i in range(n_batches):
        # New batch
        dst = 'data/batch' + (str(i + 1)) + '/'
        batch = batches5_array[i]
        print('For BATCH '+ str(i + 1))
        print(batch)
        for f in batch:
            copy2(('data/batch5/' + f + '.txt'), dst)


# -----------------------------------------------------------------------
# Source: batch_divider.ipynb, cell 13
# Change: moved from utils/visualization.py; wrapped in a function;
#         article_lengths passed as argument;
#         %matplotlib inline removed (Jupyter-only magic command)
# -----------------------------------------------------------------------
def plot_length_distribution(article_lengths):
    x = article_lengths
    plt.hist(x, density=True, bins=30, align='right')
    plt.ylabel('Frequency')
