# -*- coding: cp1251 -*-
import requests as rq
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def ending(number): #��� ��� ����, ����� ������� ������ ������� % ��������� �������
    if number % 100 == 11:
        return '�'
    number %= 10
    if number == 1:
        return ''
    else:
        return '�'

url = 'https://www.kritika24.ru/page.php?id=1907&top=kritik&cat=EGJe_2013&page='

ege_link_and_title = []
#print('����������� ������ ������ � �����������\n\n\n')
for page_num in range(1, 27): #����� ������ � 1 �� 26 ��������
    flag_page = False        #����������, ������� �� ������� ���������� �� ��������
    while not flag_page:
        try:
            page = rq.get(url + str(page_num))
        except Exception:             #����������� �������
            time.sleep(1)
            continue
        flag_page = True
    #time.sleep(1)
    soup = BeautifulSoup(page.text, features="html.parser")  #utf-8 �� ���
    #print(soup.prettify())
    #print(soup.text)
    list_ = []
    for link in soup.find_all("a"):        #������ ����������� � �������� �� � ������� �������� + ����� ���������� �� php?id=
        list_.append((str(link.get('href')), link.text))
    for link, title in list_:
        index = link.find('php?id=')
        #print(link[index + 7:])
        try:
            number = int(link[index + 7:]) #�� ���-�� �������� (����� 'page' ���� �����������)
        except ValueError:
            number = -1
        if index != -1 and link.find('EGJe') == -1 and number > 4917: #������ ����������: !== �� 0 �� 4917
            ege_link_and_title.append(('https://www.kritika24.ru/' + link, title))
    ege_link_and_title.pop() #������ ������ � �����
    ege_link_and_title.pop()
    #print(ege_link_and_title)

ege_link_and_title.pop(0) #��������� ������ ��� ���������, �.�. ��� ��� �� ��������
ege_link_and_title.pop(0)
ege_link_and_title.pop(0)
ege_list_with_essays = []
#print(ege_link_and_title)
print('�������� ���������\n\n\n')
counter = 0
len_ = len(ege_link_and_title)
len_percent = len_ // 100

for link, title in ege_link_and_title:
    if counter % (len_percent + 1) == len_percent:
        print(f'���������{ending(int(100 * counter / len_))} {int(100 * counter / len_)}% ���������\n')
    counter += 1
    flag_page = False  # ��������� �� �������� (��/���)
    while not flag_page:
        try:
            page = rq.get(link)
        except Exception:
            time.sleep(1)
            continue
        flag_page = True

    soup = BeautifulSoup(page.text, 'lxml')
    flag_img = False                       #������� ��� ������ �� �����������: ��� img + scr=screen'
    for elem in soup.find_all('img'):
        if elem['src'].startswith('screen'):
            #print(elem['src'])
            flag_img = True
    if flag_img:
        continue
    essay = '' #������� ������
    flag_K = False                   #�������� � ����������: �������� �� ���� � ������� �6 � �9
    k_6 = None
    k_9 = None
    for elem in soup.find_all('p'):
        if not flag_K:
            if elem.text.find('�1') == -1: #�� ������� �1, ��� ���� �����
                essay += elem.text
            else:
                flag_K = True         #���� ����� �1, ������ ���� ��������, � ����� �� �����
        else:
            if elem.text.find('�6') != -1:
                score_list = re.findall(r'[0-2]', elem.text)
                if len(score_list) > 0: #��� ����� 1-� �������, �.�. ������ �� ������: 2 �� 2 ��� 2/2. ���� ����� ����� ���� - ������, ������ �� ����
                    k_6 = score_list[0]

            if elem.text.find('�9') != -1:
                score_list = re.findall(r'[0-2]', elem.text)
                if len(score_list) > 0:
                    k_9 = score_list[0]
    #print(essay)
    if k_6 is not None and k_9 is not None:
        ege_list_with_essays.append((link, title, essay, k_6, k_9))


with open('Essays with K6, K9.txt', 'a') as file_: #�������� � ����
    for link, title, essay, k_6, k_9 in ege_list_with_essays:
        file_.write(essay)
        file_.write(f"\n�������� �6: {k_6}, �������� �9: {k_9}\n\n") #f ������ - ���������������, ���� �������

print(len(ege_list_with_essays))

df = pd.DataFrame(ege_list_with_essays, columns=['������', '���������', '����� ���������', '�������� �6', '�������� �9'])
#df.to_excel('table with K6,K9.xlsx')
df.to_csv('essays.csv')


