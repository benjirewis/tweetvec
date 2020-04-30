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

# senator list retreived from CSPAN https://twitter.com/cspan/lists/senators?lang=en
# party affiliations from https://www.senate.gov/senators/index.htm
party_assocation = {"SenHydeSmith": 1, "SenDougJones": 0, "SenTinaSmith": 0,
                    "SenJohnKennedy": 1, "SenCortezMasto": 0, "SenKamalaHarris": 0, 
                    "SenThomTillis": 1, "SenSasse": 1, "SenatorRounds": 1, "SenDanSullivan": 1, 
                    "sendavidperdue": 1, "SenJoniErnst": 1, "SenBrianSchatz": 0, "senatemajldr": 1, 
                    "MartinHeinrich": 0, "SenatorRisch": 1, "SenatorBaldwin": 0, "SenTedCruz": 1, 
                    "SenatorFischer": 1, "SenatorHeitkamp": 0, "SenDuckworth": 0, 
                    "SenWarren": 0, "SenTomCotton": 1, "SenatorHassan": 0, "MikeCrapo": 1, 
                    "SenatorTester": 0, "SenJackReed": 0, "SenFeinstein": 0, "SenCoonsOffice": 0, 
                    "LindseyGrahamSC": 1, "SenJohnHoeven": 1, "McConnellPress": 1, 
                    "SenJohnThune": 1, "PattyMurray": 0, "SenatorEnzi": 1, "SenBlumenthal": 0, 
                    "EnergyDems": 0, "SenDeanHeller": 1, "SenatorWicker": 1, 
                    "senorrinhatch": 1, "RonWyden": 0, "SenatorCarper": 0, "SenatorDurbin": 0, 
                    "SenatorLeahy": 0, "SenWhitehouse": 0, "SenGaryPeters": 0, "SenCoryGardner": 1, 
                    "Sen_JoeManchin": 0, "SenToddYoung": 1, "SenRonJohnson": 1, "SenateAgDems": 0, 
                    "SenatorLankford": 1, "SenBennetCO": 0, "SenToomey": 1, "SenatorTimScott": 1, 
                    "RandPaul": 1, "SenDonnelly": 0, "SenJohnBarrasso": 1, "SenCapito": 1, 
                    "timkaine": 0, "SenBobCasey": 0, "ChrisMurphyCT": 0, 
                    "SenatorCantwell": 0, "SenatorShaheen": 0, "SenatorCardin": 0, 
                    "maziehirono": 0, "SenMikeLee": 1, "EnergyGOP": 1, "SenatorIsakson": 1, 
                    "SenAlexander": 1, "SenStabenow": 0, "SenPatRoberts": 1, "SenBobCorker": 1, 
                    "SenateDems": 0, "SenGillibrand": 0, "SenatorTomUdall": 0, "BillCassidy": 1, 
                    "brianschatz": 0, "TinaSmithMN": 0, "SenSherrodBrown": 0, 
                    "amyklobuchar": 0, "SenJeffMerkley": 0, "SenMarkey": 0, 
                    "RoyBlunt": 1, "SenatorBurr": 1, "SenShelby": 1, "SenBillNelson": 0, 
                    "InhofePress": 1, "stabenow": 0, "SenatorCollins": 1, 
                    "senrobportman": 1, "SenatorMenendez": 0, "JerryMoran": 1, 
                    "ChrisVanHollen": 0, "lisamurkowski": 1, "SenSchumer": 0, "clairecmc": 0, 
                    "CoryBooker": 0, "marcorubio": 1, "ChrisCoons": 0, 
                    "GrahamBlog": 1, "SenateGOP": 1, "JohnCornyn": 1, "SteveDaines": 1, 
                    "ChuckGrassley": 1, "MarkWarner": 0, "JimInhofe": 1, "JohnBoozman": 1}

# create lists for tweets and their labels
tweets = []; tweet_labels = []

# add tweets from all senators to correct list
for senator in party_assocation.keys():
    for tweet in api.GetUserTimeline(screen_name=senator, count=200):
        t = tweet.full_text
        separate = "https"
        t_new = t.split(separate, 1)[0]
        tweets.append(t_new)
        if party_assocation[senator] == 1:
            tweet_labels.append('rep')
        else:
            tweet_labels.append('dem')

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
model_dbow.save('./out/pol_model.d2v')
