# coding: utf-8
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

url_list = ['https://lenta.ru/rubrics/russia/','https://lenta.ru/rubrics/world/','https://lenta.ru/rubrics/economics/','https://lenta.ru/rubrics/forces/','https://lenta.ru/rubrics/science/','https://lenta.ru/rubrics/culture/','https://lenta.ru/rubrics/sport/','https://lenta.ru/rubrics/media/','https://lenta.ru/rubrics/travel/']

links_clear = [] 
for url in url_list:
    text = requests.get(url, timeout=5)
    content = BeautifulSoup(text.content, "html.parser")
    links = content.find_all('div', attrs={'class':'item news b-tabloid__topic_news'}, limit = 10)
    for item in links:
        link = 'https://lenta.ru' + item.find('div', {'class': 'titles'}).find('a').get('href')
        links_clear.append(link)

links_final = [links_clear[i:i+10] for i in range(0,len(links_clear),10)] 

News_total = []
for i in links_final:
    News = []
    for j in i:
        new = requests.get(j, timeout=5)
        new_con = BeautifulSoup(new.content, "html.parser")
        new_con_text = new_con.find_all('p')
        for item in new_con_text:
            piece = item.text
            News.append(piece)
    News = str(News).lower()
    News_total.append(News)

names = ['russia.csv', 'world.csv', 'economics.csv','forces.csv', 'science.csv','culture.csv','sport.csv','media.csv','travel.csv']

final = []
for item in News_total: 
    frequency = {}
    word_count = re.findall(r'\b[а-я]{4,}\b', item)
    for word in word_count:
        count = frequency.get(word,0)
        frequency[word] = count + 1
    frequency_sorted = sorted(frequency.items(), key=lambda para:(para[1]), reverse = True)[0:20]
    final.append(frequency_sorted)

columns = ['СЛОВО','ЧАСТОТА']
for item in final:
    df = pd.DataFrame(item, columns=columns)
    df.to_csv(names[final.index(item)])
