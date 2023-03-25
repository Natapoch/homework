- * - coding: utf-8 - * -
 #убрала для гита кодировку, чтобы не слетала кодировка в комментариях, но запускала код с -*- coding: cp1251 -*-
import requests as rq
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def ending(number):     #это для того, чтобы красиво дальше считать % скачанных текстов
    if number % 100 == 11:
        return 'о'
    number %= 10
    if number == 1:
        return ''
    else:
        return 'о'

url = 'https://www.kritika24.ru/page.php?id=1907&top=kritik&cat=EGJe_2013&page='

ege_link_and_title = []
#print('Составление списка ссылок с сочинениями\n\n\n')
for page_num in range(1, 27): #нужны ссылки с 1 по 26 страницу
    flag_page = False        #показывает, удалось ли считать информацию со страницы
    while not flag_page:
        try:
            page = rq.get(url + str(page_num))
        except Exception:             #отказывался парсить
            time.sleep(1)
            continue
        flag_page = True
    #time.sleep(1)
    soup = BeautifulSoup(page.text, features="html.parser")  #utf-8 не идёт
    #print(soup.prettify())
    #print(soup.text)
    list_ = []
    for link in soup.find_all("a"):        #найдем гиперссылки и соединим их с номером страницы + семью элементами до php?id=
        list_.append((str(link.get('href')), link.text))
    for link, title in list_:
        index = link.find('php?id=')
        #print(link[index + 7:])
        try:
            number = int(link[index + 7:]) #по кол-ву символом (слово 'page' тоже учитывалось)
        except ValueError:
            number = -1
        if index != -1 and link.find('EGJe') == -1 and number > 4917: #задали промежуток: !== от 0 до 4917
            ege_link_and_title.append(('https://www.kritika24.ru/' + link, title))
    ege_link_and_title.pop() #убрали лишнее с конца
    ege_link_and_title.pop()
    #print(ege_link_and_title)

ege_link_and_title.pop(0) #исключить первые три сочинения, т.к. они нам не подходят
ege_link_and_title.pop(0)
ege_link_and_title.pop(0)
ege_list_with_essays = []
#print(ege_link_and_title)
print('Выгрузка сочинений\n\n\n')
counter = 0
len_ = len(ege_link_and_title)
len_percent = len_ // 100

for link, title in ege_link_and_title:
    if counter % (len_percent + 1) == len_percent:
        print(f'Обработан{ending(int(100 * counter / len_))} {int(100 * counter / len_)}% сочинений\n')
    counter += 1
    flag_page = False  # загружена ли страница (да/нет)
    while not flag_page:
        try:
            page = rq.get(link)
        except Exception:
            time.sleep(1)
            continue
        flag_page = True

    soup = BeautifulSoup(page.text, 'lxml')
    flag_img = False                       #убираем все ссылки на изображения: тег img + scr=screen'
    for elem in soup.find_all('img'):
        if elem['src'].startswith('screen'):
            #print(elem['src'])
            flag_img = True
    if flag_img:
        continue
    essay = '' #создали строку
    flag_K = False                   #работаем с критериями: отбираем по тегу с текстом К6 и К9
    k_6 = None
    k_9 = None
    for elem in soup.find_all('p'):
        if not flag_K:
            if elem.text.find('К1') == -1: #не найдено К1, еще идет текст
                essay += elem.text
            else:
                flag_K = True         #если нашел К1, дальше идут критерии, в текст не пишет
        else:
            if elem.text.find('К6') != -1:
                score_list = re.findall(r'[0-2]', elem.text)
                if len(score_list) > 0: #нам нужен 1-й элемент, т.к. запись мб разной: 2 из 2 или 2/2. Если длина будет ноль - значит, оценок не было
                    k_6 = score_list[0]

            if elem.text.find('К9') != -1:
                score_list = re.findall(r'[0-2]', elem.text)
                if len(score_list) > 0:
                    k_9 = score_list[0]
    #print(essay)
    if k_6 is not None and k_9 is not None:
        ege_list_with_essays.append((link, title, essay, k_6, k_9))


with open('Essays with K6, K9.txt', 'a') as file_: #добавили в файл
    for link, title, essay, k_6, k_9 in ege_list_with_essays:
        file_.write(essay)
        file_.write(f"\nКритерий К6: {k_6}, критерий К9: {k_9}\n\n") #f строка - форматированная, чтоб красиво

print(len(ege_list_with_essays))

df = pd.DataFrame(ege_list_with_essays, columns=['Ссылка', 'Заголовок', 'Текст сочинения', 'Критерий К6', 'Критерий К9'])
#df.to_excel('table with K6,K9.xlsx')
df.to_csv('essays.csv')


