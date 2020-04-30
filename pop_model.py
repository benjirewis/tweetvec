# import twitter API and JSON processor
import twitter
import json

# gensim imports.
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn import utils
import csv
import multiprocessing
import nltk
from nltk.corpus import stopwords

from __future__ import print_function

# define our accessible API object
api = twitter.Api(consumer_key='iTYLP38Z7pGv31kIg6x994IIJ',
                  consumer_secret='wxw4zrKmxhvmOlkwFI4UhVoVKWRCpZsaQH3gF8BIFoyViFHuCV',
                  access_token_key='1071489398317989889-wRuGv0r65uK8RX9wHFTrFbSRNMNgMr',
                  access_token_secret='zGa4BDFxIb3RIa7hoiVtQZLuRc9ehKd3vqMbUkkbqs2pF', tweet_mode="extended")

# Most popular users retreived from https://friendorfollow.com/twitter/most-followers/
top_accounts = [
                "BarackObama", "justinbieber", "katyperry" ,"rihanna", "taylorswift13",
                "Cristiano", "ladygaga", "TheEllenShow", "realDonaldTrump", "ArianaGrande",
                "YouTube", "jtimberlake", "KimKardashian", "selenagomez", "Twitter",
                "cnnbrk", "britneyspears", "narendramodi", "shakira", "jimmyfallon",
                "BillGates", "CNN", "neymarjr", "nytimes", "KingJames",
                "JLo", "MileyCyrus", "BrunoMars", "Oprah", "BBCBreaking",
                "SrBachchan", "iamsrk", "BeingSalmanKhan", "NiallOfficial", "Drake",
                "SportsCenter", "KevinHart4real", "wizkhalifa", "NASA", "instagram",
                "akshaykumar", "espn", "LilTunechi", "imVkohli", "Harry_Styles",
                "realmadrid", "PMOIndia", "LouisTomlinson", "elonmusk", "LiamPayne"
                "BarackObama", "justinbieber", "katyperry" ,"rihanna", "taylorswift13",
                "Cristiano", "ladygaga", "TheEllenShow", "realDonaldTrump", "ArianaGrande",
                "YouTube", "jtimberlake", "KimKardashian", "selenagomez", "Twitter",
                "cnnbrk", "britneyspears", "narendramodi", "shakira", "jimmyfallon",
                "BillGates", "CNN", "neymarjr", "nytimes", "KingJames",
                "JLo", "MileyCyrus", "BrunoMars", "Oprah", "BBCBreaking",
                "SrBachchan", "iamsrk", "BeingSalmanKhan", "NiallOfficial", "Drake",
                "SportsCenter", "KevinHart4real", "wizkhalifa", "NASA", "instagram",
                "akshaykumar", "espn", "LilTunechi", "imVkohli", "Harry_Styles",
                "realmadrid", "PMOIndia", "LouisTomlinson", "elonmusk", "LiamPayne"
                "BarackObama", "justinbieber", "katyperry" ,"rihanna", "taylorswift13",
                "Cristiano", "ladygaga", "TheEllenShow", "realDonaldTrump", "ArianaGrande",
                "YouTube", "jtimberlake", "KimKardashian", "selenagomez", "Twitter",
                "cnnbrk", "britneyspears", "narendramodi", "shakira", "jimmyfallon",
                "BillGates", "CNN", "neymarjr", "nytimes", "KingJames",
                "JLo", "MileyCyrus", "BrunoMars", "Oprah", "BBCBreaking",
                "SrBachchan", "iamsrk", "BeingSalmanKhan", "NiallOfficial", "Drake",
                "SportsCenter", "KevinHart4real", "wizkhalifa", "NASA", "instagram",
                "akshaykumar", "espn", "LilTunechi", "imVkohli", "Harry_Styles",
                "realmadrid", "PMOIndia", "LouisTomlinson", "elonmusk", "LiamPayne"
                ]

# add tweets from all senators to correct list
tweets = []
for handle in top_accounts:
    for tweet in api.GetUserTimeline(screen_name=handle, count=200):
        t = tweet.full_text
        separate = "https"
        t_new = t.split(separate, 1)[0]
        tweets.append(t_new)

# revised tokenizer.
def tokenize_text(text):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) < 2:
                continue
            tokens.append(word.lower())
    return tokens

# find number of cores for parallelization.
cores = multiprocessing.cpu_count()

# read + tokenize the tweets.
documents = []
for i,tweet in enumerate(tweets):
    documents.append(TaggedDocument(words=tokenize_text(tweet), tags=[tweet_label,i+1])

# create Doc2Vec model.
model_dbow = Doc2Vec(dm=1, vector_size=45, negative=5, hs=0, min_count=2, sample=0, workers=cores)
model_dbow.build_vocab([x for x in documents])
documents = utils.shuffle(documents) # shuffle
model_dbow.train(documents,total_examples=len(documents), epochs=30)
model_dbow.save('./out/pop_model.d2v')
