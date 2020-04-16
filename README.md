# Stock Prediction using Viral News :chart_with_upwards_trend: 
Stock Exchange is a fierce and unpredictable battleground for investors because it is extremely volatile at any given time. Attempts to predict whether a stock price will be higher or lower than it is on a given day truly is a challenging task. This stems from the fact that volatility makes it difficult to apply simple time-series or regression techniques. Even so, the challenge of stock price prediction is very appealing because a little improvement can increase profits multifold. The paper demonstrates some state-of-art methods for stock price prediction ranging from early statistical analysis to recent Machine Learning and Artificial Intelligence domains.Then, the research plan, evaluation plan, and division of work that we will follow throughout the project are specified. Extensive research and advances in these fields have made it possible to predict stock prices very effectively.

> :warning: For installation, execute instructions, screenshots and module specific functions look at the **README.md** files under each module.
> This is a general **README** file with higher level details of the project.
> Data(Amazon and Apple) hourly change data is provided to us by the Professor.
> Preprocessing extracted from data provided are stored in Semantic_Web_Mining_Project/CODE/Preprocessing.

### The Problem

● Online news portals are universal and provide a good platform for stock market related information. Such prominent information sources can be used to predict stock prices.

● Investigating related news can create early-warning indicators which can specify if a big event is going to happen or if it’s in the early stages of happening. 

● Analysing and predicting stock market using  news is difficult since it is constantly changing by the second.

● Multiple factors and combinations like physical, physiological, rational and irrational factors play a major role in the prediction of such stocks, when these factors are combined together it makes the scenario challenging and very difficult to predict with high degree of accuracy and precision.


### Algorithms

1)Logistic Regression - Logistic regression is a regression and predictive analysis to conduct when the dependent variable is dichotomous (binary).  

2)Support Vector Machine - Support Vector Machine algorithm finds a hyperplane in an N-dimensional space (N — the number of features) that distinctly classifies the data points.

3)Decision Tree - Decision Tree is supervised algorithm that expands its branches after every iteration into a tree like structure. At the end, the leaf nodes are the predictions of the model.

4)Recurrent Neural Network (RNN) - RNN is deep learning model. They are especially powerful in use cases in which context is critical to predicting an outcome. they use feedback loops to process a sequence of data that informs the final output, which can also be a sequence of data . These feedback loops allow information to persist; the effect is often described as memory.

### Preprocessing of the raw data 
There are around 76000 rows in our dataset.
We did preprocessing those raw data by Python and MySQL.
News data preprocessing: First, we extract data we need, like time, website and text, from the News data. Then we import those into new table by MySQL, because those data are not ordered, we should organize our data through MySQL by time. After that, we can get clean data and order by time. 
Stock Chart preprocessing: After we got new clean news data, we need combine them and price of two companies stocks. 


### Evaluations
● Logistic Regression and Support Vector Machine gave less accuracy. This implies:
Non - linear data
Complex model
Overfitting issue

● Decision Tree and RNN gave the best accuracy.

● Methods to improve accuracy:
There might be a class label imbalance in the train test data. K-fold cross validation can be implemented.
Values of hyper-parameters might not be optimal. Grid Search can to implemented to find the best hyper parameters.  

● On top of that UI Interfaces screenshots as well as the code is being pushed into the repo to give a big picture of our project working. It gives us the information of how accurate and good are decision tree and RNN in predicting real-time stocks.

### References

```
● Chatzis, S.P., Siakoulis, V., Petropoulos, A., Stavroulakis, E. and Vlachogiannakis, N., 2018.  Forecasting stock market crisis events using deep and statistical machine learning techniques. Expert Systems with Applications, 112, pp.353-371.
● Tsinaslanidis, P.E., 2018. Subsequence dynamic time warping for charting: Bullish and bearish class predictions for NYSE stocks. Expert Systems with Applications, 94, pp.193-204.
● Pagolu, Venkata Sasank, Kamal Nayan Reddy, Ganapati Panda, and Babita Majhi., 2016. Sentiment Analysis of Twitter Data for Predicting Stock Market Movements. Paper presented at the 2016 International Conference on Signal Processing, Communication, Power and Embedded System (SCOPES), Paralakhemundi, India, October 3–5.
● Selvin, S., Vinayakumar, R., Gopalakrishnan, E.A., Menon, V.K. and Soman, K.P., 2017, September. Stock price prediction using LSTM, RNN and CNN-sliding window model. In 2017 international conference on advances in computing, communications and informatics (icacci) (pp. 1643-1647). IEEE.
```

### Q & A

**Q.1:  Why do you consider Neural Networks to be the best method for predicting real-time stocks? 
Ans.** Neural Networks are a key piece of some of the most successful machine learning algorithms. The development of neural networks have been key to teaching computers to think and understand the world in the way that humans do. Essentially, a neural network emulates the human brain.Here to predict Neural Networks we used RNN neural network for predicting real time stocks.You can look at the accuracy, it is considered to be a great tools for predicting real time stocks.

**Q.2: Why did you using sentiment analysis?
Ans.** The sentiment is tagged for the News articles based on the occurrence of positive and negative keywords
with the ticker or stock symbols. The Sentistrength package is used with an exhaustive corpus and a financial dictionary - Loughran
and McDonald Financial Sentiment Dictionaries [12] to check for the occurrences of the keywords and a sentiment score is assigned
to each News article in the corresponding time frame. The combination of keywords such as "increased", "went up", "crashed" etc, are
2 considered along with the presence of financial related keywords for tagging the sentiment of the news data.

**Q.3:Why is n-gram being used instead of bag of words?
Ans.** N-gram is being considered to be better instead of bag of words because firstly it identify the best time frame for prediction,it also identify the best feature extraction methods. On top of that it ie very effiecient for this project because it ranks the news source,as well as rank tweets.


