import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def preprocess():
	df = pd.read_csv('featureMatrix(amazon and apple).csv')
	df1 = df[df['Company Stocks'] == 1]
	X = df1[['Semantic Analysis']]
	y = df1[['Amazon']]

	return X,y

def ImplementDecisionTree(X,y):
	tree = DecisionTreeClassifier()
	tree.fit(X,y)
	predicted_classes_1 = tree.predict(X)
	accuracy = accuracy_score(y,predicted_classes_1)
	print("Accuracy: ",str(accuracy*100)+"%")


if __name__ == '__main__':
	X,y = preprocess()
	ImplementDecisionTree(X,y)