import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import tensorflow as tf


# 1 amazon, 2 apple
# 1 hour --> ac = 87.51%, f1 = 81%
# 4 hours --> ac = 85.49%, f1 = 80.95%
def get_value():
	df = pd.read_csv('Updated_2_featureMatrix(amazon and apple).csv', encoding='latin-1')
	# df = pd.read_csv('featureMatrix(amazon and apple).csv', encoding='latin-1')
	df1 = df.loc[(df['Company Stocks'] == 1) | (df['Company Stocks'] == 3)]
	y = df1[['Positive semantic']].values
	X = df1['Text'].values
	return X, y


def rnn(X, y):
	# preprocessing data
	tk = Tokenizer(lower=True)
	tk.fit_on_texts(X)
	X_seq = tk.texts_to_sequences(X)
	X_pad = pad_sequences(X_seq, maxlen=100, padding='post')

	X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.25, random_state=0)
	batch_size = 64
	X_train1 = X_train[batch_size:]
	y_train1 = y_train[batch_size:]
	X_valid = X_train[:batch_size]
	y_valid = y_train[:batch_size]

	vocabulary_size = len(tk.word_counts.keys())+1

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

	# evaluate the training model
	accuracy = model.evaluate(X_test, y_test)
	print(accuracy)

	# calculate F1 score
	yhat_classes = model.predict_classes(X_valid, verbose=0)
	f1 = f1_score(y_valid, yhat_classes)
	print('F1 score: %f' % f1)


if __name__ == '__main__':
	X, y = get_value()
	rnn(X, y)
