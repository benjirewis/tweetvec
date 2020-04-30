import twitter
import json

api = twitter.Api(consumer_key='iTYLP38Z7pGv31kIg6x994IIJ',
                  consumer_secret='wxw4zrKmxhvmOlkwFI4UhVoVKWRCpZsaQH3gF8BIFoyViFHuCV',
                  access_token_key='1071489398317989889-wRuGv0r65uK8RX9wHFTrFbSRNMNgMr',
                  access_token_secret='zGa4BDFxIb3RIa7hoiVtQZLuRc9ehKd3vqMbUkkbqs2pF',
                  tweet_mode="extended")

tp_accounts = [
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

def sanitize_tweet(tweet: String):
    """
    takes a `tweet` and returns a sanitized version.
    :param tweet: the tweet to be sanitized
    :return: the sanitzed tweet
    """
    split_tweet = twokenize.tokenize(tweet)
    sntzd = []
    for word in split_tweet:
        if word not in stop_words:
            sntzd.append(word)
    return ' '.join(sntzd)


def get_tweets(handle: String)
    """
    returns 200 most recents tweets from `handle` account.
    :param handle: account to be accessed
    :return: list of 200 most recent tweets from `handle`
    """
    tweets = []
    separate = "https"

    for tweet in api.GetUserTimeline(screen_name=handle, count=200):
        t = tweet.full_text
        t_new = t.split(separate, 1)[0] # Remove "https" tag.
        t_new = sanitize_tweet(t_new)
        tweets.append(t_new)

    return tweets
