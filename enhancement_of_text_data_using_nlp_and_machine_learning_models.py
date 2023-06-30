# -*- coding: utf-8 -*-
"""Enhancement_of_Text_Data_Using_NLP_And_Machine_Learning_Models.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uEYgpuYaaqR9IF260a50h_QBHqBXrBL_

# **Installation Important Libraries**
"""

!pip install datasets

!pip install textattack

!pip install tensorflow_text

#Required Modules
import re
import string
import numpy as np
import pandas as pd
import nltk
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from matplotlib import pyplot
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
import time 
from keras.layers import Activation, Dense, Dropout, Embedding, Flatten, Conv1D, MaxPooling1D, SimpleRNN, SpatialDropout1D
from tensorflow.keras import layers
import tensorflow as tf

"""# **Load Dataset**"""

from datasets import list_datasets, load_dataset
from pprint import pprint

datasets_list = list_datasets()

from datasets import load_dataset
datasets = load_dataset('snips_built_in_intents')
print(datasets)

"""# **Converting to DataFrame**"""

print(datasets['train'][0])

print(datasets['train'][0]['text'])
print(datasets['train'][0]['label'])

print(datasets['train']['text'])

dataset = pd.DataFrame(list(zip(datasets['train']['text'],datasets['train']['label'])),columns=['text','label'])
print(dataset)

dataset.label.unique()

labels = dataset['label'].values.tolist()
sort_label = dataset['label'].unique()
sort_label.sort()
for l in sort_label:
    print(l , ": " , labels.count(l))

"""# **Pre-Processing**"""

#Converting to lowercase
sentences = dataset['text']
print("Before lowercase:", sentences[0])
sentences = [sentence.lower() for sentence in sentences]
print("After lowercase:", sentences[0])

#Removing emoticons and punctuation
print("Before Removing Punctuation and Emoticons: ", sentences[0])
sentences = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in sentences]
print("After Removing Punctuation and Emoticons: ", sentences[0])

#Splitting into list (Removing whitespaces)
print("Before splitting:", sentences[0])
sentences = [sentence.split() for sentence in sentences]
print("After splitting:", sentences[0])

#Lemmatization
lemmatizer = nltk.WordNetLemmatizer()
print("Before Lemmatization: ", sentences[0])
filtered_sentences = []
for words in sentences:
  filtered_words = []
  for word in words:
    filtered_words.append(lemmatizer.lemmatize(word))
  filtered_sentences.append(filtered_words)
sentences = filtered_sentences    
print("After Lemmatization: ", sentences[0])

sentences = [' '.join(map(str, sentence)) for sentence in sentences]

dataset['sentences'] = sentences
dataset = dataset.drop(['text'], axis=1)

dataset.head()

"""# **Train Test Split**"""

from sklearn.model_selection import train_test_split
train, test = train_test_split(dataset, test_size = 0.10, random_state = 42)
print(len(train))
print(len(test))

labels = train['label'].values.tolist()
sort_label = train['label'].unique()
sort_label.sort()
for l in sort_label:
    print(l , ": " , labels.count(l))

"""# **Amplification of data**

## **Embedding Augmenter**
"""

from textattack.augmentation import EmbeddingAugmenter

print(train['sentences'][150])
s = train['sentences'][150]
aug = EmbeddingAugmenter()
ss = aug.augment(s)
print(ss)

train_aug = train.copy()
aug = EmbeddingAugmenter()
train_aug['sentences'] = train_aug['sentences'].apply(lambda x: str(aug.augment(x)))
train = train.append(train_aug, ignore_index=True)

train.tail()

#Removing [] and ''
sentences = train['sentences']
print("Before Removing Punctuation and Emoticons: ", sentences[580])
sentences = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in sentences]
print("After Removing Punctuation and Emoticons: ", sentences[580])

train = train.drop(['sentences'], axis=1)
train['sentences'] = sentences

len(train)

"""## **WordNet Augmenter**"""

from textattack.augmentation import WordNetAugmenter

train_aug = train.copy()
aug = WordNetAugmenter()
train_aug['sentences'] = train_aug['sentences'].apply(lambda x: str(aug.augment(x)))
train = train.append(train_aug, ignore_index=True)

#Removing [] and ''
sentences = train['sentences']
print("Before Removing Punctuation and Emoticons: ", sentences[580])
sentences = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in sentences]
print("After Removing Punctuation and Emoticons: ", sentences[580])

train = train.drop(['sentences'], axis=1)
train['sentences'] = sentences

train.tail()

len(train)

"""## **EasyData Augmenter**"""

from textattack.augmentation import EasyDataAugmenter

print(train['sentences'][100])

s = train['sentences'][100]
aug = EasyDataAugmenter()
ss = aug.augment(s)
print(ss)

train_aug = pd.DataFrame(columns=['sentences','label'])
aug = EasyDataAugmenter()
for index, row in train.iterrows():
    aug_sentences = aug.augment(row['sentences'])
    for s in aug_sentences:
       train_aug = train_aug.append({'sentences': s, 'label': row['label']},ignore_index=True)
train = train.append(train_aug, ignore_index=True)

train.tail()

len(train)

"""## **CheckList**"""

from textattack.augmentation import CheckListAugmenter

print(train['sentences'][50])
s = train['sentences'][50]
aug = CheckListAugmenter(pct_words_to_swap=0.5, transformations_per_example=2)
ss = aug.augment(s)
print(ss)

train_aug = train.copy()
aug = CheckListAugmenter(pct_words_to_swap=0.5, transformations_per_example=1)
train_aug['sentences'] = train_aug['sentences'].apply(lambda x: str(aug.augment(x)))
train = train.append(train_aug, ignore_index=True)

train.tail()

#Removing [] and ''
sentences = train['sentences']
print("Before Removing Punctuation and Emoticons: ", sentences[580])
sentences = [sentence.translate(str.maketrans('', '', string.punctuation)) for sentence in sentences]
print("After Removing Punctuation and Emoticons: ", sentences[580])

train = train.drop(['sentences'], axis=1)
train['sentences'] = sentences

train.tail()

"""# **Tokenization**"""

# The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 50000
# Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 250
# This is fixed.
EMBEDDING_DIM = 100
tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
tokenizer.fit_on_texts(dataset['sentences'].values)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))

X_train = tokenizer.texts_to_sequences(train['sentences'].values)
X_train = pad_sequences(X_train, maxlen=MAX_SEQUENCE_LENGTH)
X_test = tokenizer.texts_to_sequences(test['sentences'].values)
X_test = pad_sequences(X_test, maxlen=MAX_SEQUENCE_LENGTH)
print('Shape of data tensor:', X_train.shape)

Y_train = pd.get_dummies(train['label']).values
Y_test = pd.get_dummies(test['label']).values
print('Shape of label tensor:', Y_train.shape)

"""#**Preparing data for Model**"""

df = pd.DataFrame(list(zip(datasets['train']['text'],datasets['train']['label'])),columns=['text','label'])
print(df)

df['label'].value_counts(normalize=True)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vector = TfidfVectorizer(lowercase=True, #this will convert all the tokens into lower case
                         stop_words='english', #remove english stopwords from vocabulary. if we need the stopwords this value should be None
                         analyzer='word', #tokens should be words. we can also use char for character tokens
                         max_features=50000, #maximum vocabulary size to restrict too many features
                         min_df = 5,
                         max_df = .6
                        )

tfidf_vectorized_corpus = tfidf_vector.fit_transform(df.text)

tfidf_vectorized_corpus

print (tfidf_vectorized_corpus.shape)

"""# **Classification with a minimal use of ML techniques**"""

df['label'].value_counts(normalize=True)

"""The process of TF-IDF vectorization entails determining the TF-IDF score for each word in your corpus in relation to that document and then storing that data as a vector."""

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vector = TfidfVectorizer(lowercase=True, #this will convert all the tokens into lower case
                         stop_words='english', #remove english stopwords from vocabulary. if we need the stopwords this value should be None
                         analyzer='word', #tokens should be words. we can also use char for character tokens
                         max_features=50000, #maximum vocabulary size to restrict too many features
                         min_df = 5,
                         max_df = .6
                        )

tfidf_vectorized_corpus = tfidf_vector.fit_transform(df.text)

tfidf_vectorized_corpus

print (tfidf_vectorized_corpus.shape)

"""#**Logistic Regression**"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold

lg = LogisticRegression(multi_class='auto',solver='lbfgs')
cv_scores = cross_val_score(X=tfidf_vectorized_corpus,y=df.label,cv=5,estimator=lg)
print (cv_scores, np.mean(cv_scores),np.std(cv_scores))

cv_scores = cross_val_score(X=tfidf_vectorized_corpus,y=df.label,cv=StratifiedKFold(5,random_state=42,shuffle=True),estimator=lg)
print (cv_scores, np.mean(cv_scores),np.std(cv_scores))

from sklearn.naive_bayes import MultinomialNB

nb = MultinomialNB()
cv_scores = cross_val_score(X=tfidf_vectorized_corpus,y=df.label,cv=5,estimator=nb)
print (cv_scores, np.mean(cv_scores),np.std(cv_scores))

cv_scores = cross_val_score(X=tfidf_vectorized_corpus,y=df.label,cv=StratifiedKFold(5,random_state=42,shuffle=True),estimator=nb)
print (cv_scores, np.mean(cv_scores),np.std(cv_scores))

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=101, random_state=42) #n_estimator is the parameter to control number of decision tress
cv_scores = cross_val_score(X=tfidf_vectorized_corpus,y=df.label,cv=5,estimator=model)
print (cv_scores, np.mean(cv_scores),np.std(cv_scores))

cv_scores = cross_val_score(X=tfidf_vectorized_corpus,y=df.label,cv=StratifiedKFold(5,random_state=42,shuffle=True),estimator=model)
print (cv_scores, np.mean(cv_scores),np.std(cv_scores))

for train_idx, val_idx in StratifiedKFold(n_splits=5,random_state=42,shuffle=True).split(tfidf_vectorized_corpus,df.label.values):
    break

trainX = tfidf_vectorized_corpus[train_idx]
valX = tfidf_vectorized_corpus[val_idx]
trainy = df.label.values[train_idx]
valy = df.label.values[val_idx]

print (trainX.shape, valX.shape)

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

lg = LogisticRegression(multi_class='auto',solver='lbfgs')
lg.fit(trainX,trainy)

val_train= lg.predict(trainX)
val_pred = lg.predict(valX)

print ("Accuracy score: {}".format(accuracy_score(trainy,val_train)))
print ("F1 score: {}".format(f1_score(trainy,val_train,average='macro')))

print ("Accuracy score: {}".format(accuracy_score(valy,val_pred)))
print ("F1 score: {}".format(f1_score(valy,val_pred,average='macro')))

import matplotlib.pyplot as plt
import seaborn as sns

def plot_cm(y_true, y_pred, labels, title):
    figsize=(14,10)
    cm = confusion_matrix(y_true, y_pred, labels=np.unique(labels))
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_perc = cm / cm_sum.astype(float) * 100
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_perc[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = '%.1f%%\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.1f%%\n%d' % (p, c)
    cm = pd.DataFrame(cm, index=np.unique(y_true), columns=np.unique(y_true))
    cm.index.name = 'Actual'
    cm.columns.name = 'Predicted'
    fig, ax = plt.subplots(figsize=figsize)
    plt.title(title)
    sns.heatmap(cm, cmap='viridis', annot=annot, fmt='', ax=ax)

#print (confusion_matrix(valy, val_pred,labels=model.classes_))
labels = lg.classes_
plot_cm(valy,val_pred,labels,'Confusion matrix: F1 {}'.format(f1_score(valy,val_pred,average='macro')))

"""# Analyses of the Model"""

!pip install eli5

import eli5

eli5.show_weights(lg, vec=tfidf_vector, top=25)

df.iloc[val_idx[:3]]['text']

df.text.values[val_idx[9]]

eli5.show_prediction(lg, doc=df.text.values[val_idx[9]], vec=tfidf_vector, top=10)