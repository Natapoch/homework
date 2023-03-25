import pandas as pd
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

def clean_texts(texts, stop_words):
    texts_str = texts.lower() # нижний регистр
    texts_list_nltk = word_tokenize(texts_str) # токенизация
    texts_without_punkt = [word for word in texts_list_nltk
                           if word[0].isalpha()] # удалить пунктуацию из списка токенов
    texts_clean = [word for word in texts_without_punkt if word not in stop_words] # чистим от стоп-слов
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


with open('Клише для ЕГЭ.txt', 'r', encoding = 'utf-8') as cliche:
    cliches = (cliche.read())


def unique_words_amount(text):
    return len(set(text))


ege_essays = pd.read_csv("essays3.csv", encoding="utf-8", sep=',')
index_name = ege_essays.columns[0]
ege_essays = ege_essays.set_index(index_name)


list_df_k6 = [ege_essays[ege_essays['Критерий К6'] == i] for i in range(3)]

stop_words = stopwords.words('russian')
stop_words.extend(['критерий', 'к6', 'к9', 'который', 'это', 'k6', 'k9', 'из-за', 'он', 'её', 'его', 'их', 'ее'])
new_stop_words = stop_words.copy()
new_stop_words.extend(lemmatized_texts(cliches, stop_words))

average = []

for df_ in list_df_k6:
    sum_ = 0
    for number in range(len(df_)):
        new_text = lemmatized_texts(df_.iloc[number]['Текст сочинения'], new_stop_words)
        sum_ += unique_words_amount(new_text)
    average.append(sum_/len(df_))
for i in range(len(average)):
    print(f'Среднее количество уникальных слов в сочинениях с критерием К6 {i}: {average[i]}\n')