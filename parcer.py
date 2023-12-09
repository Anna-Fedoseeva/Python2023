import requests
import sqlite3 as sl
from time import sleep
from bs4 import BeautifulSoup

con = sl.connect('parcer.db') #�������� ���� ������ parser

url = 'https://habr.com/ru/hubs/'

sql = 'INSERT INTO HABR (name, dicription, rating, subscribers,link) values(?, ?, ?, ?, ?)' # �������������� ������������� ������ 

data = [] # list ��� ������ � �����

for p in range(1,12):
    url = f'https://habr.com/ru/hubs/page{p}/' # �������� �������� ������
    r = requests.get(url)
    sleep(3)
    soup = BeautifulSoup(r.text, "html.parser")

    habs = soup.findAll('div', class_= 'tm-hubs-list__category-wrapper')
    for hab in habs:
      link = 'https://habr.com/ru/hubs/' + hab.find('a', class_='tm-hub__title').get('href') # �������� ������
      name =hab.find('a', class_='tm-hub__title').text # �������� �������� ����
      dicription =hab.find('div', class_='tm-hub__description').text # �������� ����
      rating = hab.find('div', class_= 'tm-hubs-list__hub-rating').text # �������
      subscribers =hab.find('div', class_= 'tm-hubs-list__hub-subscribers').text # ����������
      data.append([name, dicription, rating, subscribers,link]) # ��������� ��� ������ � �����
    


data1 = con.execute("select count(*) from sqlite_master where type='table' and name='HABR'") # ������� �������
for row in data1:
   if row[0] == 0:
      with con: #
                con.execute("""
                    CREATE TABLE HABR (
                        name VARCHAR(100) PRIMARY KEY,
                        dicription STRING,
                        rating STRING,
                        subscribers STRING,
                        link STRING
                    );
                """)
with con: # � ������� �������������� ������� ��������� ��� ������
   con.executemany(sql, data)


with con: # ������� ����������� �������
    data2 = con.execute("SELECT * FROM HABR")
    for row in data2:
        print(row)