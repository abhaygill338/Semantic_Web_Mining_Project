import pandas as pd
import numpy as np
from keras.engine.saving import load_model
from keras.losses import mean_squared_error
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

scaler = MinMaxScaler(feature_range=(0, 1))


# 2 apple, 1 amazon
# 'featureMatrix.csv to four hours -->
# 'Updated_2_featureMatrix(amazon and apple).csv' to one hour --> 88.13%
def get_value():
    df = pd.read_csv('Updated_2_featureMatrix(amazon and apple).csv', encoding='latin-1')
    # df = pd.read_csv('featureMatrix(amazon and apple).csv', encoding='latin-1')
    df1 = df.loc[(df['Company Stocks'] == 2) | (df['Company Stocks'] == 3)]
    y = df1[['Positive semantic']].values
    X = df1['Text'].values
    return X, y


def rnn(X, y):
    # preprocessing data
    tk = Tokenizer(lower=True)
    tk.fit_on_texts(X)
    X_seq = tk.texts_to_sequences(X)
    X_pad = pad_sequences(X_seq, maxlen=100, padding='post')
    # to normalize the dataset
    # X_nor = scaler.fit_transform(X_pad)
    # print(len(X_pad))
    # print(y)  32912

    X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.25, random_state=0)
    batch_size = 64
    X_train1 = X_train[batch_size:]
    y_train1 = y_train[batch_size:]
    X_valid = X_train[:batch_size]
    y_valid = y_train[:batch_size]

    vocabulary_size = len(tk.word_counts.keys()) + 1
    # print(vocabulary_size) 85024

    # create the model
    max_words = 100
    embedding_size = 32
    model = Sequential()
    model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
    model.add(Dropout(0.5))
    model.add(LSTM(200))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train1, y_train1, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=5)
    # model.save('stock_apple.h5')
    # model = load_model('stock_apple.h5')

    # model predict
    y_predict = model.predict(X_test)
    print(y_predict)

    # evaluate the training model
    accuracy = model.evaluate(X_test, y_test)
    print(accuracy)
    # print("model mean squared error is " + str(mean_squared_error(y_test, y_predict)))


if __name__ == '__main__':
    X, y = get_value()
    rnn(X, y)
