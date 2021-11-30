#!/usr/bin/env python3

import PyPDF2
import sys
import os
from pathlib import Path
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('wordnet')
import spacy
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def merge_dataset(PATH):

    files_paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.txt']
    my_df = []
    for file_path in files_paths:
        filename = Path(file_path).stem

        with open(file_path) as f:
            lines = f.read()
        d = {
            'filename' : filename,  # some formula for obtaining values
            'text' : lines,
        }
        my_df.append(d)
    my_df = pd.DataFrame(my_df)
    return my_df

def text_process(text):
    '''
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Return the cleaned text as a list of words
    4. Remove words
    '''
    stemmer = spacy.load('fr_core_news_md')

    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join([i for i in nopunc if not i.isdigit()])
    nopunc =  [word.lower() for word in nopunc.split() if word not in stopwords.words('french')]
    

    return [stemmer.lemmatize(word) for word in nopunc]



def main():
    PATH="../extracted_text/"
    my_df = merge_dataset(PATH)

    # my_df.to_csv('../all_dataset.csv', index=False)



    title = list(my_df["filename"])
    wiki_lst = list(my_df["text"])

    vectorizer = TfidfVectorizer(stop_words={'french'})
    X = vectorizer.fit_transform(wiki_lst)



    Sum_of_squared_distances = []
    K = range(2,10)
    for k in K:
       km = KMeans(n_clusters=k, max_iter=200, n_init=10)
       km = km.fit(X)
       Sum_of_squared_distances.append(km.inertia_)
    # plt.plot(K, Sum_of_squared_distances, 'bx-')
    # plt.xlabel('k')
    # plt.ylabel('Sum_of_squared_distances')
    # plt.title('Elbow Method For Optimal k')
    # plt.show()

    true_k = 3
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    labels=model.labels_
    wiki_cl=pd.DataFrame(list(zip(title,labels)),columns=['filename','cluster'])


    write_wiki_cl = wiki_cl.sort_values(by=['cluster'])

    # write_wiki_cl.to_csv('../files_clustering.csv', index=False)


    result={'cluster':labels,'wiki':wiki_lst}
    result=pd.DataFrame(result)
    for k in range(0,true_k):
        s=result[result.cluster==k]
        text=s['wiki'].str.cat(sep=' ')
        text=text.lower()
        text=' '.join([word for word in text.split()])
        wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
        print('Cluster: {}'.format(k))
        print('Titles')
        titles=wiki_cl[wiki_cl.cluster==k]['filename']         
        print(titles.to_string(index=False))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

if __name__ == '__main__':
    main()