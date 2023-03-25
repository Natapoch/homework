import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def clean_texts(texts, stop_words):
    texts_str = texts.lower() # ������ �������
    texts_list_nltk = word_tokenize(texts_str) # �����������
    texts_without_punkt = [word for word in texts_list_nltk
                           if word[0].isalpha()] # ������� ���������� �� ������ �������
    texts_clean = [word for word in texts_without_punkt if word not in stop_words] # ������ �� ����-����
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


with open('Essays with K6, K9.txt', 'r') as all_essays:
    texts = all_essays.read()
with open('����� ��� ���.txt', 'r', encoding = 'utf-8') as cliche:
    cliches = (cliche.read())


stop_words = stopwords.words('russian')
stop_words.extend(['��������', '�6', '�9', '�������', '���', 'k6', 'k9', '��-��', '��', '�', '���', '��', '��'])

lemmatized_texts_ = lemmatized_texts(texts, stop_words)
wordcloud = WordCloud().generate(', '.join(lemmatized_texts_))
plt.imshow(wordcloud) # ��� ����������
plt.axis("off") # ��� �������� �� ����
plt.show() # �������� �����������
print(wordcloud)



new_stop_words = stop_words.copy()
new_stop_words.extend(lemmatized_texts(cliches, stop_words))
#words_lemmatized = lemmatized_texts(texts, stop_words)
#print(stop_words)
#print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
#print(new_stop_words)

new_lemmatized_texts = lemmatized_texts(texts, new_stop_words)
new_wordcloud = WordCloud().generate(', '.join(new_lemmatized_texts))
plt.imshow(new_wordcloud)
plt.axis("off")
plt.show()
print(new_wordcloud)
