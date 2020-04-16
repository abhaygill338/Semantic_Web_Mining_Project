# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 00:05:05 2020

@author: palas
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing,svm
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score,f1_score,precision_recall_curve,classification_report
from sklearn.model_selection import train_test_split


# READING DATA AND EXTRACTING RELEVANT COLUMNS
df = pd.read_csv('Updated_2_featureMatrix(amazon and apple).csv')
df1 = df.loc[(df['Company Stocks'] == 2) | (df['Company Stocks'] == 3)]
X = df1[['Semantic Analysis','AccuracySites']].values
y = df1[['Apple']].values


#PLOTTING THE TARGET TO SEE THE RATIO OF POSTIVES AND NEGATIVES
df1['Apple'].value_counts()
sns.countplot(x='Apple',data = df1, palette = 'hls')


#PLOTTING FEATURES AGAINST THE LABELS
sns.set_style('whitegrid')
sns.countplot(x='Apple', hue='Semantic', data=df1)


# PRINT THE PERCENTAGE OF NEGATIVES AND POSITIVES
stock_dec = len(df1[df1['Apple']== -1])
stock_inc = len(df1[df1['Apple']== 1])
pct_stock_dec = stock_dec/(stock_dec+stock_inc)
print("Percentage of stock decrease is", pct_stock_dec*100)
pct_stock_inc = stock_inc/(stock_inc+stock_dec)
print("percentage of stock increase is", pct_stock_inc*100)


#DECISION TREE
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)
min_max_scaler = preprocessing.MinMaxScaler()
x_train_scaled = min_max_scaler.fit_transform(X_train)
x_test_scaled = min_max_scaler.fit_transform(X_test)
tree = DecisionTreeClassifier()
tree.fit(X,y)
y_pred = tree.predict(X_test)
y_train_pred = tree.predict(X_train)
print('Training accuracy %s' % accuracy_score(y_train, y_train_pred))
print('Testing F1 score: {}'.format(f1_score(y_train, y_train_pred, average='weighted')))
print('Testing accuracy %s' % accuracy_score(y_test, y_pred))
print('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))


#PLOT PRECISION VS RECALL
def plot_prec_recall_vs_tresh(precisions, recalls, thresholds):
    plt.plot(thresholds, precisions[:-1], 'b--', label='precision')
    plt.plot(thresholds, recalls[:-1], 'g--', label = 'recall')
    plt.xlabel('Threshold')
    plt.legend(loc='upper left')
    plt.ylim([0,1])

pre, rec, thresholds = precision_recall_curve(y_test, tree.predict_proba(X_test)[:,1])
plot_prec_recall_vs_tresh(pre, rec, thresholds)
plt.figure()


#DECSION TREE REPORT
report = classification_report(y_test,y_pred,output_dict=True)
report_df = pd.DataFrame(report).transpose()


