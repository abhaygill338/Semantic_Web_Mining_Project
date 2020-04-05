import pymysql
import psycopg2
import csv

def creat_db():
    con = pymysql.connect(host='127.0.0.1', user='root',
                          passwd='babu1', charset='utf8',use_unicode=True)
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS chart;')
    cur.execute('CREATE DATABASE IF NOT EXISTS chart;')
    con.commit()
    con.close()
# def getOpenConnection(user='postgres', password='babu1', dbname='postgres1'):
#     return psycopg2.connect("dbname='" + dbname + "' user='" + user + "' host='localhost' password='" + password + "'")

def creat_tb(title, site, date, text):
    con = pymysql.connect(host='127.0.0.1', user='root',
                          passwd='babu1', db='chart', charset='utf8',use_unicode=True)
    cur = con.cursor()
    try:
        with con:
            cur.execute("CREATE TABLE IF NOT EXISTS News(Id INT PRIMARY KEY AUTO_INCREMENT, Title varchar(1500), Site char("
                        "255), Date char(40), Text varchar(5000))")
            cur.execute(
                'INSERT INTO News(Title, Site, Date, Text) VALUES(%s, %s, %s, %s)', (title, site, date, text))

        con.commit()
    except Exception as e:
        con.rollback()
        print(e)

    con.commit()
    con.close()

def export_hourly_data(filepath):
    con = pymysql.connect(host='127.0.0.1', user='root',
                          passwd='babu1', db='chart', charset='utf8')
    cur = con.cursor()
    i = 0
    #
    while i < 10:
        print(i)
        try:
            cur.execute("SET @dt = '2018-1-01 00:00:00'")
            cur.execute("SET @dt1 = '%s'", i)
            cur.execute("SET @dt2 = '%s'", i+1)

            cur.execute("SELECT Title,Site, date_format(Date,'%Y-%m-%d %H:%i:%s') FROM News WHERE Date >= "
                        "date_add(@dt, INTERVAL @dt1 HOUR) AND  DATE < date_add(@dt, INTERVAL @dt2 HOUR) ORDER BY "
                        "Date ASC")

            results = cur.fetchall()
            export_data_toFile(results, filepath)
            for r in results:
                print(r)
            
            con.commit()
        except Exception as e:
            con.rollback()
            print(e)
        i = i+1
    con.close()

# export data to csv file
def export_data_toFile(results, filepath):
    with open(filepath, 'a+', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in results:
            csvwriter.writerow(row)

