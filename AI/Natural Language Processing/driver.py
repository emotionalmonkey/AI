import numpy as np
import pandas as pd
from os import path, listdir
import string
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV

#train_path = "../resource/lib/publicdata/aclImdb/train/" # use terminal to ls files under this directory
#test_path = "../resource/lib/publicdata/imdb_te.csv" # test data for grade evaluation

train_path = path.join(path.dirname(__file__),"aclImdb/train/")
test_path = path.join(path.dirname(__file__),"imdb_te.csv")

with open(path.join(path.dirname(__file__),"stopwords.en.txt"), "r") as f:
    stopwords = set(f.read().split("\n"))

def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
	and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''
    
    with open(outpath + name, "w", encoding = "ISO-8859-1") as train_csv:
        train_csv.write("row_number,text,polarity\n")
        count = 0
        for folder in listdir(inpath):
            if folder != "pos" and folder != "neg":
                continue
            polarity = "1" if folder == "pos" else "0"
            for file in listdir(path.join(inpath,folder)):
                with open(path.join(inpath,folder,file), "r", encoding = "ISO-8859-1") as input:
                    text = input.read().replace("<br />"," ")

                    # format text - remove stopwords & punctuations
                    punctuation_remover = str.maketrans('', '', string.punctuation)
                    text = text.translate(punctuation_remover)
                    text = " ".join([ t for t in text.split() if t.lower() not in stopwords])
                    #print(len(text))

                    train_csv.write(str(count) + "," + text + "," + polarity + "\n")            
                    count += 1  
    
    df = pd.read_csv(outpath + name, encoding = "ISO-8859-1")  
    return df

def write_output(filename, predictions):
    with open(filename, "w") as f:
        for p in predictions:
            f.write(str(p) + "\n")    
  
def classify(train_df, test_df, ngram, alpha):
    corpus = train_df["text"]
    polarity = train_df["polarity"]
    test_corpus = test_df["text"]
    filename = "unigram" if ngram == (1, 1) else "bigram"

    count_clf = Pipeline([('vect', CountVectorizer(stop_words=stopwords, ngram_range=ngram)),
                          ('clf', SGDClassifier(loss='hinge', penalty='l1', alpha=alpha[0], fit_intercept=False))]).fit(corpus, polarity)
    
    predictions = count_clf.predict(test_corpus)
    write_output(filename + ".output.txt", predictions)
    print(np.mean(predictions == polarity))

    tfidf_clf = Pipeline([('vect', TfidfVectorizer(stop_words=stopwords, ngram_range=ngram)),                     
                          ('clf', SGDClassifier(loss='hinge', penalty='l1', alpha=alpha[1], fit_intercept=False))]).fit(corpus, polarity)
   
    predictions = tfidf_clf.predict(test_corpus)
    write_output(filename + "tfidf.output.txt", predictions)   
    print(np.mean(predictions == polarity))
    """
    parameters = {'vect__ngram_range': [(1, 1), (1, 2)],         
                  'tfidf__use_idf': (False, True),
              'clf__alpha': (1e-2, 1e-3, 1e-4)}

    test_clf = Pipeline([('vect', CountVectorizer()),      
                         ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l1'))])
    gs_clf = GridSearchCV(test_clf, parameters, n_jobs=-1)
    gs_clf = gs_clf.fit(corpus,polarity)
    print(gs_clf.best_score_)
    print(gs_clf.best_params_)
    predictions = gs_clf.predict(test_corpus)
    print(np.mean(predictions == polarity)) 
    """

if __name__ == "__main__":
    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''
  	
    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    bigram.output.txt'''
     
    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigramtfidf.output.txt'''
  	
    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to bigramtfidf.output.txt'''
     
    train_df = imdb_data_preprocess(train_path)
    test_df = pd.read_csv(test_path, encoding = "ISO-8859-1")
    #unigram
    classify(train_df, test_df, (1, 1), [0.0002, 0.0002])
    #bigram
    classify(train_df, test_df, (1, 2), [1e-05, 2e-05])
    


