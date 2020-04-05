from datetime import datetime, timedelta
import json
import os, glob
import string
import create_sql
import csv
import sys


import numpy as np
from nltk import word_tokenize, PorterStemmer
from nltk.corpus import stopwords


def preprocess_data(text):
    # remove space
    sentence = text.strip()
    # remove white space
    prooned = sentence.strip()

    # remove stopwords and number
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if w not in stop_words]
    filtered_sentence = [w for w in filtered_sentence if not w.isdigit()]

    # remove punctuation and lowercase
    table = str.maketrans('', '', string.punctuation)
    sentence = [w.translate(table).lower() for w in filtered_sentence]

    # stem word
    porter = PorterStemmer()
    sentence = [porter.stem(word) for word in sentence]
    result = ','.join(sentence)
    return result


def time_fix(dt):
    date = dt[:23]
    dif = dt[23:]
    pos = dif.find(':')
    dif = timedelta(hours=int(dif[:pos]), minutes=float(dif[pos + 1:]))
    if dt[23] == '-':
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f') - dif
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f') + dif
    return date


def write_file(filepath):
    test = open(filepath, 'w')
    my_files = []
    my_files2 = []
    counter_files = 0
    # rootdir = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\Data\News'
    rootdir = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\Data\News\2018_01_d157b48c57be246ec7dd80e7af4388a2'

    for subdirectory, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdirectory + os.sep + file
            if filepath.endswith(".json"):
                # print (file, "\nentire path:" + filepath)
                my_files.append(str(file))
                my_files2.append(str(filepath))
                counter_files += 1

    print("File #:", counter_files)
    create_sql.creat_db()
    for i in my_files2:
        with open(i, 'r', errors='ignore') as f:
            # print(i)
            data = json.load(f)
            text = preprocess_data(data['text'])
            title = data['thread']['title']
            site = data['thread']['site']
            date1 = time_fix(data['thread']['published'])
            date = time_fix(data['thread']['published']).strftime("%Y,%m,%d,%H,%M,%S")
            print(date)
            # print(title)
            inset_db(title, site, date1, text)
            lists = '[' + title + ']' + ', [' + site + '], [' + date + '], [' + text + '] \n'
        test.write(lists + '\n')
        # print(lists)
    test.close()


def inset_db(title, site, date, text):
    create_sql.creat_tb(title, site, date, text)

def openClose(chart_filename):
    chartData = open(chart_filename, 'a+')
    reader = csv.reader(chartData)
    for row in reader:
        print(row)
    chartData.close()

def timeNewsCorr(newsData, stockDatApple, stockDatAmazon):

    newsData1 = open(newsData, 'r', errors='ignore')
    appleData = open(stockDatApple, 'r', errors='ignore')
    amazonData = open(stockDatAmazon, 'r', errors='ignore')

    news_totalData = []
    news_reader = csv.reader(newsData1)
    for line in news_reader:
        news_totalData.append(line[0])
    # print(news_totalData[0], "\n")

    apple_date = []
    apple_totalDataStart = []
    apple_totalDataEnd = []
    appleReader = csv.reader(appleData)
    for line in appleReader:
        apple_date.append(line[0])
        apple_totalDataStart.append(line[2])
        apple_totalDataEnd.append(line[5])
    # print("Apple: " ,apple_totalDataStart[0] ,"\n", apple_totalDataStart[0], "\n", apple_totalDataEnd[0],"\n" , apple_date[0])
    
    amazon_date = []
    amazon_time = []
    amazon_totalDataStart = []
    amazon_totalDataEnd = []
    amazonReader = csv.reader(amazonData)
    for line in amazonReader:
        amazon_date.append(line[0])
        amazon_time.append(line[1])
        amazon_totalDataStart.append(line[2])
        amazon_totalDataEnd.append(line[5])
    # print("Amazon: ", amazon_totalDataStart[0] ,"\n", amazon_totalDataStart[0], "\n", amazon_totalDataEnd[0],"\n" , amazon_date [0], "\n" , amazon_time[0])

    counter = 0
    
    for row in news_totalData:
        # print(row )
        counter2 = 0  
        # print(row)  
        news_date_var = datetime.strptime(row, "%Y-%m-%d %H:%M:%S")
        print("news date:",news_date_var)
        for row2 in amazon_date:
            first = datetime.strptime(amazon_date[counter]+ "," + amazon_time[counter], "%Y.%m.%d,%H:%M")
            # 2018-01-01 12:0:0->  2018-01-01 13:0:0  12:30-20:20
            # if >=12:30 <=20:20 
            # if compare indx new with indx amz
            if (news_date_var >= first): 
                print("Found date: " ,row , "||", first )

            counter2 +=1
        # print(amazon_date[counter] + " " + amazon_time[counter])
        counter+=1

# folder_path = '/Users/matthewbao/Desktop/study/CSE573/News/2018_01_d157b48c57be246ec7dd80e7af4388a2'
txt_filename = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\test.txt'
# write_file(txt_filename)
chart_filename = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Data\CHARTS\AMAZON60.csv'
# openClose(chart_filename)
newsData1 = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\test1.csv'
stockDataApple1 = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\Data\CHARTS\APPLE60.csv'
stockDataAmazon1 = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\Data\CHARTS\AMAZON60.csv'
timeNewsCorr(newsData1, stockDataApple1, stockDataAmazon1)
    
