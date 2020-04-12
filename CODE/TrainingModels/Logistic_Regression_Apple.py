import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def preprocess():
	df = pd.read_csv('featureMatrix(amazon and apple).csv')
	df1 = df[df['Company Stocks'] == 2]
	X = df1[['Semantic Analysis']]
	y = df1[['Apple']]

	return X,y

def ImplementLogisticRegression(X,y):
	model = LogisticRegression()
	model.fit(X,y)
	predicted_classes = model.predict(X)
	accuracy = accuracy_score(y,predicted_classes)
	print("Accuracy: ",str(accuracy*100)+"%")


if __name__ == '__main__':
	X,y = preprocess()
	ImplementLogisticRegression(X,y)



