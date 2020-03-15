import matplotlib.pyplot as plt
import tweepy
from textblob import TextBlob
import re


class EmoAnalysis:

    def __init__(self):
        self.tweets = []

    def ptage(self, part, whole):

        return 100 * float(part) / float(whole)

    def downloaddata(self):

        consumerkey = "4SLqqB8mdfjqLdwv42IBzyCIM"
        consumersecret = "yaVSOxfX39HsW8oNI1exwCigZV2fYlgzSNgQnCBgE7qI0LhW3v"
        accesstoken = "2543940913-hXequh6434VfNMjX6vMr64YjMNTY1GjH3UiUl4x"
        accesstokensecret = "xpcZ5BeUuH9BjVc6AqeZMu6IbbQVln9vCFxZUgylqZBJE"

        auth = tweepy.OAuthHandler(consumer_key=consumerkey, consumer_secret=consumersecret)
        auth.set_access_token(accesstoken, accesstokensecret)
        api = tweepy.API(auth)

        searchterm = input("Enter term to be searched about: ")
        noofsearchterms = int(input("enter number of tweets to be searched: "))

        self.tweets = tweepy.Cursor(api.search, q=searchterm, lang="English").items(noofsearchterms)

        positive = 0
        negative = 0
        neutral = 0
        polarity = 0

        for tweet in self.tweets:
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity
            if analysis.sentiment.polarity == 0:
                neutral += 1
            elif analysis.sentiment.polarity > 0:
                positive += 1
            elif analysis.sentiment.polarity < 0:
                negative += 1

        positive = self.ptage(positive, noofsearchterms)
        negative = self.ptage(negative, noofsearchterms)
        neutral = self.ptage(neutral, noofsearchterms)

        positive = format(positive, '.2f')
        negative = format(negative, '.2f')
        neutral = format(neutral, '.2f')

        if polarity == 0:
            print("Neutral")
        if polarity == 1:
            print("Positive")
        if polarity == -1:
            print("Negative")

        self.plotpiechart(positive, negative,  neutral, searchterm, noofsearchterms)

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def plotpiechart(self, positive, negative, neutral, searchterm, noofsearchterms):

        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
        sizes = [positive, negative, neutral]
        colors = ['yellowgreen', 'gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchterm + ' by analyzing ' + str(noofsearchterms) + ' Tweets.')
        plt.axis('scaled')
        plt.tight_layout()
        plt.show()

if __name__== "__main__":
    sa = EmoAnalysis()
    sa.downloaddata()


