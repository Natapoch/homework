import pandas as pd
from nltk.corpus import stopwords
import re
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
from nltk.tokenize import word_tokenize, wordpunct_tokenize


def clean_texts(texts, stop_words):
    texts_str = texts.lower()
    texts_list_nltk = word_tokenize(texts_str)
    texts_without_punkt = [word for word in texts_list_nltk
                           if word[0].isalpha()]
    texts_clean = [word for word in texts_without_punkt if word not in stop_words]
    return texts_clean


def lemmatized_texts(texts, stop_words):
    words_lemmatized = []
    for word in clean_texts(texts, stop_words):
        result = morph.parse(word)
        most_probable_result = result[0]
        normal_form = most_probable_result.normal_form
        if normal_form not in stop_words:
            words_lemmatized.append(normal_form)
    return words_lemmatized


def unique_words_amount(text):
    return len(set(text)) #вернули длину множества

def average_sentence_len(text):
    #print(text)
    sentence_list = re.split('[а-я][\.\!\?]', text)  #будет съедать последнюю букву в слове, но для нас это не так важно. А вот когда инициал с точкой принимает за конец предложения - это уже проблема.
    sum_ = 0 #длина, сколько слов во всех предложениях текста
    amount_ = 0 #сколько всего предложений в тексте
    #print(sentence_list)
    for sentence in sentence_list:
        sum_ += len(sentence.split()) #разбили на слова и добавили в переменную длину предложения (кол-во слов)
        if len(sentence.split()) > 0: #убрали пустые предложения без слов
            amount_ += 1         #считаем предложения
    #print(sum_, amount_)
    return sum_ / amount_          #среднее


ege_essays = pd.read_csv("essays3.csv", encoding="utf-8", sep=',') #обращаемся к датафрейму
index_name = ege_essays.columns[0]
ege_essays = ege_essays.set_index(index_name)
#print(ege_essays)

list_df_k6 = [ege_essays[ege_essays['Критерий К6'] == i] for i in range(3)] #разбиваем по оценкам (3 датафрейма по баллу)
list_df_k9 = [ege_essays[ege_essays['Критерий К9'] == i] for i in range(3)]
#print(len(list_df_k6[0]))
stop_words = stopwords.words('russian')
average = []

for df_ in list_df_k6:
    sum_ = 0   #переменная, в которой будет сумма всех чисел уникальных слов
    for number in range(len(df_)):
        new_text = lemmatized_texts(df_.iloc[number]['Текст сочинения'], stop_words) #вызвали элемент в строке через iloc + лемматизировали
        sum_ += unique_words_amount(new_text)
    #print(len(df_))
    average.append(sum_/len(df_))
for i in range(len(average)):
    print(f'Среднее количество уникальных слов в сочинениях с критерием К6 {i}: {average[i]}\n')


average = []
for df_ in list_df_k6:
    sum_ = 0
    for number in range(len(df_)):
        sum_ += average_sentence_len(df_.iloc[number]['Текст сочинения'])
    #average_sentence_len(df_.iloc[number]['Текст сочинения'])
    #print(len(df_))
    average.append(sum_/len(df_))
for i in range(len(average)):
    print(f'Среднее количество слов в предложении в сочинениях с критерием К6 {i}: {average[i]}\n')

average = []
for df_ in list_df_k9:
    sum_ = 0
    for number in range(len(df_)):
        sum_ += average_sentence_len(df_.iloc[number]['Текст сочинения'])
    #average_sentence_len(df_.iloc[number]['Текст сочинения'])
    #print(len(df_))
    average.append(sum_/len(df_))
for i in range(len(average)):
    print(f'Среднее количество слов в предложении в сочинениях с критерием К9 {i}: {average[i]}\n')


