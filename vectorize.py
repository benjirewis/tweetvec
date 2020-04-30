from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn import utils
import csv
import multiprocessing
import nltk
from nltk.corpus import stopwords

import twitter

from .reference/classify_util import get_polarization

from sklearn.manifold import TSNE
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
import numpy as np
from mpl_toolkits import mplot3d

import json
import numpy as np

from __future__ import print_function
import sys


# change default encoding to account for accents.
stdout = sys.stdout
sys.setdefaultencoding('utf-8')
sys.stdout = stdout

# extract document vectors + types.
n = len(documents)
ids = [x for x in range(1,n+1)]
cind_types = [type_dict[x] for x in range(1,n+1)]
cind_X = model_dbow[ids]

# retrieved from http://www.cs.jhu.edu/~mdredze/datasets/multiview_embeddings/.
# not present on Git repo; file too large.
USER_GRAPH_FILE = "./data/user_graph"
pol_model = Doc2Vec.load("./out/pol_model")
pop_model = Doc2Vec.load("./out/pop_model")

class UserEmbedding(object):
    def __init__(self, handle):
        self.handle = handle
        self.tweets = self.get_tweets(handle)

        self.pol_vector = pol_model.infer_vector(tweets, epochs=10)
        self.pop_vector = pop_model.infer_vector(tweets, epochs=10)
        self.user_vector = [0 for _ in range(45)] # initialize as empty 45-vector.
        with open(USER_GRAPH_FILE) as graph:
            self.user_vector = graph.lookup(handle)

        self.final_vector = np.add(user_vector, np.add(pol_vector, pop_vector))
        flat_tweets = [t for s in tweets for t in s]
        self.sent = get_polarization(flat_tweets)

    def get_tweets(handle)
        tweets = []
        separate = "https"

        for tweet in api.GetUserTimeline(screen_name=handle, count=200):
            t = tweet.full_text
            t_new = t.split(separate, 1)[0] # Remove "https" tag.
            t_new = sanitize_tweet(t_new)
            tweets.append(t_new)

        return tweets

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 vectorize.py HANDLE")

    handle = sys.argv[1].strip('@')
    e = UserEmbedding(handle)

    # print(e.final_vector)
