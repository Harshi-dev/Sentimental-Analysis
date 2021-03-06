# -*- coding: utf-8 -*-
"""sentiment_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OJPyXlgs5XFGhQL-ic_eBL068uvGts_i
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

from google.colab import drive
import re
# %matplotlib inline
#step 1: import your libraries

drive.mount('/content/drive')#step 2: mounting data

"""# New Section"""

train_data = pd.read_table('/content/drive/MyDrive/ML/train/train.tsv')
#step 2

from google.colab import drive
drive.mount('/content/drive')

train_data.head(7)
 #step3(optional)

clean_data = train_data.loc[:,['Phrase', 'Sentiment']]#cleaning step 1:removing unnecessary columns
# Data Preprocessing with regular expression
clean_data['Phrase']= clean_data['Phrase'].str.replace(',','')
clean_data['Phrase'] = clean_data['Phrase'].str.replace('.', '')
clean_data['Phrase'] = clean_data['Phrase'].str.replace('\'ll', ' will')#change
clean_data['Phrase'] = clean_data['Phrase'].str.replace('.', '')#change

# clean_data['Sentiment'] = clean_data['Sentiment'].replace(1, 0)
# clean_data['Sentiment'] = clean_data['Sentiment'].replace(3, 4)
clean_data['Sentiment'] = clean_data['Sentiment'].apply(str)#change


clean_data['Sentiment'] = clean_data['Sentiment'].str.replace('0', 'negative') #change
clean_data['Sentiment'] = clean_data['Sentiment'].str.replace('1', 'less negative')#change
clean_data['Sentiment'] = clean_data['Sentiment'].str.replace('2', 'neutral')#cahnge
clean_data['Sentiment'] = clean_data['Sentiment'].str.replace('3', 'less positive')#change
clean_data['Sentiment'] = clean_data['Sentiment'].str.replace('4', 'positive')#change
print(clean_data['Phrase'][0])
print(clean_data.head())
#step 4: cleaning our data

''' 
If some data is missing in our data set then it is managed using some methods:
1. by removing that data from dataset
2. by predicting values using regression and decision tree.
3. by adding global constant at thar plaxe
4. by adding the one that is most frquent in our dataset
5. by adding the value by calculating the mean of the data. 
'''

clean_data['Phrase'].describe()

clean_data["Sentiment"].unique()

'''print(clean_data['Sentiment'].value_counts(), "\n")
smol_data = clean_data.sample(20000)
print("\n",len(smol_data))
print(smol_data['Sentiment'].value_counts())
clean_data = smol_data'''
clean_data = clean_data[clean_data['Sentiment'] != 'neutral']
smol_data = clean_data.sample(20000)
clean_data = smol_data
print(clean_data['Sentiment'].value_counts())
vocab_size = max([len(s) for s in clean_data['Phrase']])
print(vocab_size)

text = clean_data.Phrase.values
print(text)
#step 5: we take our clean training data and put it into an array of strings

from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=5000) #it defines most frequent top 5000 words only will be taken
tokenizer.fit_on_texts(text)  
# lower integer means more frequent words..
#this fit on text basically assigns vocabuary index based on word frequency...
word_index=tokenizer.word_index
print(word_index)
print(len(word_index))
# basically tells the no of unique tokens
#step 6: tokenizing data(assigning each word a number)
#step 1: tensorflow keras prepreocessing library

encoded_text = tokenizer.texts_to_sequences(text)
# here basically m assigning each word to its id assigned  above
# this function basically takes each word and replaces it with index value
print(encoded_text)
#step 7= conervting to numbers

from keras.preprocessing.sequence import pad_sequences
padded_sequence = pad_sequences(encoded_text)
# the sentences in our dataset is of different length, now it could pose a problem for our model in undersatnading dso we try to make the
# length of each sentence same using padding....for paddding we have a no 0 assigned for it..
print(padded_sequence[9])
#step 8: padding the matrix
print(len(clean_data['Phrase']))

from keras.models import Sequential
from keras.layers import LSTM,Dense, Dropout, SpatialDropout1D,Flatten#change in lmbda and cov2d,dense
from keras.layers import Embedding


embedding_vector_length = 32  # dimensions of output embedding vector
vocab_size = len(clean_data['Phrase']) 
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length, input_length=200))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid')) # 1 denotes the shape of layer and activatio function is the function operation to be applied.
# we are training our dataset now
model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy']) # metric is just to look at, it has nothing to do with 
# optimizer, optimizer is basically learning rate
print(model)
# print(model.summary())
#print(model.Embedding(1))

#change

'''model = Sequential()
model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(140,320,3)))
model.add(Conv2D(24, 5,strides=(2, 2), activation='elu'))
model.add(Conv2D(36, 5, strides=(2, 2), activation='elu'))
model.add(Conv2D(48, 5, strides=(2, 2), activation='elu'))
model.add(Conv2D(64, 3, activation='elu'))
model.add(Conv2D(64, 3, activation='elu'))
model.add(Dropout(0.7))
model.add(Flatten())
model.add(Dense(100, activation='elu'))
model.add(Dense(50, activation='elu'))
model.add(Dense(10, activation='elu'))
model.add(Dense(1))
model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])'''



y_train =clean_data['Sentiment']
#print(y_train)
y_train = y_train.factorize() #helps to get the numeric representation of an array by identifying distinct values.
print(y_train)
#padded_sequence = np.array(padded_sequence)
#padded_sequence = np.asarray(padded_sequence)
y_train = np.array(y_train)
#y_train = y_train.reshape(2,1)
#y_train = np.asarray(y_train).astype('float32')
#y_train = tf.convert_to_tensor(y_train)
print(y_train.shape)
print(y_train[1]) #  shape is 2 which is one is 1,0 that is sentiments and other is positive, negeative and so on
#print(type(y_train[0]))
y_train[0] = np.asarray(y_train[0]).astype('int64')
#print(y_train)
count = 0
#for value in y_train[0]:
#  print(y_train[0][value])
#  count+= 1
#print(count)
#step 10: factorising the data so we can feed it to the fir function in tensorflow

#history = model.fit(padded_sequence, y_train[0])
#history = model.fit(padded_sequence,y_train[0])
history = model.fit(padded_sequence,y_train[0],batch_size= 340,epochs=1)
#step 11: model training

plt.plot(history.history['accuracy'], label='acc')
plt.plot(history.history['val_accuracy'], label='val_acc')
plt.legend()
plt.show()

plt.savefig("Accuracy plot.jpg")

def predict_sentiment(text):
    tw = tokenizer.texts_to_sequences([text])
    tw = pad_sequences(tw,maxlen=200)
    prediction = int(model.predict(tw).round().item())
    print("Predicted label: ", y_train[1][prediction])
test_sentence1 = "this is good"
predict_sentiment(test_sentence1)
test_sentence2 = "This is a bad"
predict_sentiment(test_sentence2)
#step 12:model prediction

from sklearn.linear_model import LogisticRegression
#x_train = 
#y_train = clean_data['Sentiment'] 
padded_sequence = np.array(padded_sequence)
y_train

model = LogisticRegression()
model.fit(padded_sequence, y_train)

for i in range (2):
  print(y_train[1][i])

for i in range (10):
  print(y_train[0][i])

print(y_train[1][3])

