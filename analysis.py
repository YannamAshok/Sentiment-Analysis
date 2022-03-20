import pandas as pd
import nltk   
import sys                          
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')
nltk.download('punkt')
def analytics(file_name):
    S = SentimentIntensityAnalyzer()
    data = pd.read_csv(file_name)
    positive = list()
    negative = list() 
    polarity_list = list()
    for d in data.iterrows():
        if d[1]["Count"] >= 1 :
            token = nltk.word_tokenize(d[1]["Word"])
            if S.polarity_scores(token[0])["compound"] > 0:
                positive.append(token[0])
                polarity_list.append(S.polarity_scores(token[0])["compound"])
            elif S.polarity_scores(token[0])["compound"] < 0:
                negative.append(token[0])
                polarity_list.append(S.polarity_scores(token[0])["compound"])

    if len(positive)>len(negative):
        print("*** This product is having more positive reviews ***")
    elif len(negative)> len(positive):
        print("*** This product is having more negative reviews ***")
    values= [len(positive), len(negative)]
    labels = ["Positive words","Negative words"]
    #fig=plt.figure()
    plt.bar(labels,values,color = ['green','red' ])
    plt.savefig('report.png')
    plt.show()
    plt.scatter(polarity_list,polarity_list,color={'green'})
    plt.savefig('scatter_plot.png')
    plt.show()

if __name__ == '__main__':
    analytics(str(sys.argv[1]))