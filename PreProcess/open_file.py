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
    apple_delta = []
    appleReader = csv.reader(appleData)
    for line in appleReader:
        apple_date.append(line[0])
        apple_totalDataStart.append(line[2])
        apple_totalDataEnd.append(line[5])
        apple_delta.append(line[7])
    # print("Apple: " ,apple_totalDataStart[0] ,"\n", apple_totalDataStart[0], "\n", apple_totalDataEnd[0],"\n" , apple_date[0])
    
    amazon_date = []
    amazon_time = []
    amazon_totalDataStart = []
    amazon_totalDataEnd = []
    amazon_delta = []
    amazonReader = csv.reader(amazonData)
    for line in amazonReader:
        amazon_date.append(line[0])
        amazon_time.append(line[1])
        amazon_totalDataStart.append(line[2])
        amazon_totalDataEnd.append(line[5])
        amazon_delta.append(line[7])
    # print("Amazon: ", amazon_totalDataStart[0] ,"\n", amazon_totalDataStart[0], "\n", amazon_totalDataEnd[0],"\n" , amazon_date [0], "\n" , amazon_time[0])

    start_Time = datetime.strptime("12:30", "%H:%M")
    end_Time = datetime.strptime("21:30", "%H:%M")
    # print(start_Time, " ", end_Time)
    amazon_delta_complete = []
    apple_delta_complete = []
    flag = 0
    for counter, row in enumerate(news_totalData):
        flag = 0
        news_date_var = datetime.strptime(row, "%Y-%m-%d %H:%M:%S")
        # print("news date:",news_date_var)
        for counter2, row2 in enumerate(amazon_date):
            first_amazon = datetime.strptime(row2+ "," + amazon_time[counter2], "%Y.%m.%d,%H:%M")
            # print(news_date_var , " ", first.date())
            if (news_date_var.date() == first_amazon.date()): 
                # if it is in 13:30-21:30
                if(news_date_var.time() >= start_Time.time() and news_date_var.time() < end_Time.time()):
                    news_date_var2 = news_date_var + timedelta(hours=1)
                    if(news_date_var.time() <= first_amazon.time() and news_date_var2.time() > first_amazon.time()):
                        amazon_delta_complete.append(amazon_delta[counter2])
                        # print("found exact hr:" , first_amazon.time() , "||" ,news_date_var )
                        # print(amazon_delta[counter2], "counter:" , counter, "||", counter2)
                        flag = 1
                # this accounts for not in 13:30-21:30 so +1 day 1st hr
                else:
                    temp = news_date_var + timedelta(days=1)
                    # temp2 = temp.strptime(temp+"12:30" , "%Y:%M:%d %H:%M")
                    temp2 = temp.replace(hour=13, minute=30)
                    temp3 = temp2.strptime(row, "%Y-%m-%d %H:%M:%S")
                    for counter3, row3 in enumerate(amazon_date):
                        first_amazon2 = datetime.strptime(row3+ "," + amazon_time[counter3], "%Y.%m.%d,%H:%M")
                        # print("hey:" , first_amazon2 , "||", temp2)
                        # if(temp2.date() == first_amazon2.date() and temp2.time() == first_amazon2.time()):
                        if(temp2 == first_amazon2 and flag != 1):
                            amazon_delta_complete.append(amazon_delta[counter3])
                            print("Found 2 ", news_date_var, "||+1 day", temp2, "||amazon: " , first_amazon2)
                            print(amazon_delta[counter3], "counter", counter , "||", counter3)
                            flag = 1
                            
        # this accounts for holidays/if not in amazon do +1 day and 13:30 and give that 
        if (flag == 0):
            temp3 = news_date_var + timedelta(days=1)
            temp4 = temp3.replace(hour=13, minute=30)
            # print("holiday:", news_date_var, "||", temp4)
            for counter4, row4 in enumerate(amazon_date):
                    first_amazon3 = datetime.strptime(row4 + "," + amazon_time[counter4], "%Y.%m.%d,%H:%M")
                    # print("hey:" , first_amazon3 , "||", temp4)
                    if(temp4.date() == first_amazon3.date()):
                        # print("time", temp2.time(), first_amazon2.time())
                        if(temp4.time() == first_amazon3.time()):
                            amazon_delta_complete.append(amazon_delta[counter4])
                            # print("Found 3 ", news_date_var, "||+1 day", temp4, "||amazon: " , first_amazon3)
                            # print(amazon_delta[counter4], "counter", counter , "||", counter4)            

    # print(amazon_delta_complete[67])
     

# folder_path = '/Users/matthewbao/Desktop/study/CSE573/News/2018_01_d157b48c57be246ec7dd80e7af4388a2'
txt_filename = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\test.txt'
# write_file(txt_filename)
chart_filename = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Data\CHARTS\AMAZON60.csv'
# openClose(chart_filename)
newsData1 = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\test1.csv'
stockDataApple1 = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\Data\CHARTS\APPLE60.csv'
stockDataAmazon1 = r'C:\Users\babuvgiridar\OneDrive - Arizona State University\Asu\Year\Master\Spring 2020\Cse 573\Project\Project_preprocess\Data\CHARTS\AMAZON60.csv'
timeNewsCorr(newsData1, stockDataApple1, stockDataAmazon1)
    
