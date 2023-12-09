import requests
import sqlite3 as sl
from time import sleep
from bs4 import BeautifulSoup

con = sl.connect('parcer.db') #создание базы данных parser

url = 'https://habr.com/ru/hubs/'

sql = 'INSERT INTO HABR (name, dicription, rating, subscribers,link) values(?, ?, ?, ?, ?)' # подготавливаем множественный запрос 

data = [] # list для данных с сайта

for p in range(1,12):
    url = f'https://habr.com/ru/hubs/page{p}/' # изменяем страницу ссылки
    r = requests.get(url)
    sleep(3)
    soup = BeautifulSoup(r.text, "html.parser")

    habs = soup.findAll('div', class_= 'tm-hubs-list__category-wrapper')
    for hab in habs:
      link = 'https://habr.com/ru/hubs/' + hab.find('a', class_='tm-hub__title').get('href') # получаем ссылку
      name =hab.find('a', class_='tm-hub__title').text # получаем название хаба
      dicription =hab.find('div', class_='tm-hub__description').text # описание хаба
      rating = hab.find('div', class_= 'tm-hubs-list__hub-rating').text # рейтинг
      subscribers =hab.find('div', class_= 'tm-hubs-list__hub-subscribers').text # подписчики
      data.append([name, dicription, rating, subscribers,link]) # сохраняем все данные с сайта
    


data1 = con.execute("select count(*) from sqlite_master where type='table' and name='HABR'") # создаем таблицу
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
with con: # с помощью множественного вопроса добавляем все данные
   con.executemany(sql, data)


with con: # выводим сождержимое таблицы
    data2 = con.execute("SELECT * FROM HABR")
    for row in data2:
        print(row)