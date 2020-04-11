import csv
import pymysql

# defined init database
def init():
    con = pymysql.connect(host='127.0.0.1', user='root',
                          passwd='babu1', charset='utf8')
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS chart;')
    cur.execute('CREATE DATABASE IF NOT EXISTS chart;')
    con.commit()
    con.close()


# create new 'chart' table
def insert_news(title, site, date, text):
    con = pymysql.connect(host='127.0.0.1', user='root', 
    passwd='babu1', db='chart', charset='utf8')
    # , use_unicode=True
    cur = con.cursor()
    
    with con:
        cur.execute('CREATE TABLE IF NOT EXISTS News(Id INT PRIMARY KEY AUTO_INCREMENT, Title varchar(150), Site char('
                    '50), Date datetime, Text varchar(500))')
        cur.execute('INSERT INTO News(Title, Site, Date, Text) VALUES(%s, %s, %s, %s)', (title, site, date, text))

    con.commit()
    con.close()


def insert_chart():
    con = pymysql.connect(host='127.0.0.1', user='root',
                          passwd='babu1', db='chart', charset='utf8')
    cur = con.cursor()

    with con:
        cur.execute('CREATE TABLE IF NOT EXISTS APPL(DATE char(50), Time char(50), Open char(10), High char(10), '
                    'Low char(10), Close char(10), fq char(15), Label char(5))')
        # cur.execute("LOAD DATA INFILE '/Users/matthewbao/Desktop/study/CSE573/CHARTS/AMAZON60.csv' INTO TABLE "
        #             "APPL fields terminated by ',' optionally enclosed by '"' escaped by '"' lines terminated by '\r\n'")
    con.commit()
    con.close()


# insert news hourly
def div_hourly_data(filepath, num):
    con = pymysql.connect(host='127.0.0.1', user='root',
                          passwd='babu1', db='chart', charset='utf8')
    cur = con.cursor()
    i = 0
    k = 0
    res = open(filepath, 'w')

    while k < num-1:
        try:
            # set begin time and set the time interval (can change i+2 in two hours data)
            cur.execute("SET @dt = '2017-12-8 00:00:00'")
            cur.execute("SET @dt1 = '%s'", i)
            cur.execute("SET @dt2 = '%s'", i + 1)
            cur.execute("SELECT date_format(Date,'%Y.%m.%d %H:%i:%s'), Site, Text FROM News WHERE Date > "
                        "date_add(@dt, INTERVAL @dt1 HOUR) AND  DATE <= date_add(@dt, INTERVAL @dt2 HOUR) ORDER BY "
                        "Date ASC")

            results = cur.fetchall()
            res = export_data_toFile(results, filepath)
            # for r in results:
            #     print(r)

            con.commit()
        except Exception as e:
            con.rollback()
            # print(e)
        i = i + 1
        k = k + len(results)
        
    res.close()
    con.close()


# export data to csv file
def export_data_toFile(results, filepath):
    with open(filepath, 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if len(results) != 0:
            for row in results:
                csvwriter.writerow(row)
    return csvfile

