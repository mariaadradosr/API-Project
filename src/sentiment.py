import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import pandas as pd

def getChatSentiment(chat, coll, coll_messages):
    sid = SentimentIntensityAnalyzer()
    m = coll_messages.find({'chat_id':chat})
    out = {}
    for message in m :
        sentence = message['markdown'].encode('latin-1').decode('utf-8')
        out[sentence] = sid.polarity_scores(sentence)
    return out


def getChatPDF(out):
    outDf = pd.DataFrame(out).T
    
    mu = outDf.describe()['compound']['mean']
    sigma = outDf.describe()['compound']['std']
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)

    fig, ax = plt.subplots(figsize=(5,3.5), dpi= 80)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color='grey',  lw=4, label='norm pdf')
    ax.set_title(f'Compound conversation \n Probability density function\n ', size=12, color ='black')
    ax.axvline(x=mu, color='grey', label=str(mu)[:5])
    ax.axvline(x=mu - 2*sigma, color='orange', linestyle = '--', label=str(stats.norm.cdf(mu-2*sigma,mu, sigma)*100)[:4])
    ax.axvline(x=mu + 2*sigma, color='green',  linestyle = '--',label=str(stats.norm.cdf(mu+2*sigma,mu, sigma)*100)[:4])
    ax.legend()
    ax.spines['top'].set_color('#a8a4a2')
    ax.spines['right'].set_color('#a8a4a2')
    ax.spines['bottom'].set_color('#a8a4a2')
    ax.spines['left'].set_color('#a8a4a2')

def getChatEvol(out):
    outDf = pd.DataFrame(out).T
    y = outDf['compound']
    x = range(len(y))
    
    fig, ax = plt.subplots(figsize=(7,4), dpi= 80)

    ax.plot(x,y, c='grey', marker = 'o', markersize = 3)
    ax.fill_between(x[1:], y[1:], 0, where=y[1:] >= 0, facecolor='green', interpolate=True, alpha=0.7)
    ax.fill_between(x[1:], y[1:], 0, where=y[1:] <= 0, facecolor='red', interpolate=True, alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title("Chat Compound Score Evolution\n", fontsize=12)
    ax.set_ylabel('compound score')
    ax.set_xlabel('messages')
    ax.grid(color='grey', linestyle='-', linewidth=0.4, alpha=0.5)
    ax.spines['bottom'].set_color('#a8a4a2')
    ax.spines['left'].set_color('#a8a4a2')