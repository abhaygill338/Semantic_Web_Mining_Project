# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:40:33 2020

@author: palash
"""

#IMPORTING REQUIRED LIBRARIES
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve


# READING DATA AND EXTRACTING RELEVANT COLUMNS
df = pd.read_csv('Updated_2_featureMatrix(amazon and apple).csv')
df1 = df.loc[(df['Company Stocks'] == 1) | (df['Company Stocks'] == 3)]
X = df1[['Semantic Analysis','AccuracySites']].values
y = df1[['Amazon']].values


#PLOTTING THE TARGET TO SEE THE RATIO OF POSTIVES AND NEGATIVES
df1['Amazon'].value_counts()
sns.countplot(x='Amazon',data = df1, palette = 'hls')
plt.show()
plt.savefig('count_plot_amazon')


# PRINT THE PERCENTAGE OF NEGATIVES AND POSITIVES
stock_dec = len(df1[df1['Amazon']== -1])
stock_inc = len(df1[df1['Amazon']== 1])
pct_stock_dec = stock_dec/(stock_dec+stock_inc)
print("Percentage of stock decrease is", pct_stock_dec*100)
pct_stock_inc = stock_inc/(stock_inc+stock_dec)
print("percentage of stock increase is", pct_stock_inc*100)


# lOGISTIC REGRESSION
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)
min_max_scaler = preprocessing.MinMaxScaler()
x_train_scaled = min_max_scaler.fit_transform(X_train)
x_test_scaled = min_max_scaler.fit_transform(X_test)
logreg = LogisticRegression()
logreg.fit(X_train,y_train)
y_pred = logreg.predict(X_test)
y_train_pred = logreg.predict(X_train)
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
    plt.show()

pre, rec, thresholds = precision_recall_curve(y_test, logreg.predict_proba(X_test)[:,1])
plot_prec_recall_vs_tresh(pre, rec, thresholds)
plt.figure()

#LOGISTIC REGRESSION REPORT
report = classification_report(y_test,y_pred,output_dict=True)
report_df = pd.DataFrame(report).transpose()
print(report_df)