import csv
import re
import nltk
nltk.download('stopwords')
import nltk
nltk.download('wordnet')
import nltk
nltk.download('punkt')
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.append('I')
stop_words.append('nt')

from collections import Counter
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

def file_trans():
    with open("Copy_of_sentence_anaysis_product_edit.csv", "r", encoding='UTF-8') as f:
        reader = csv.reader(f)
        list = [e[2].strip().split(",") for e in reader if e]
    str_list = []
    str_list.extend([x[0] for x in list])
    str_list.remove("open")

    file = open('Copy_of_sentence_anaysis_product_edit.txt', 'w', encoding='UTF-8')
    file.write(str(str_list))
    file.close()
    return file

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def clean_word():
    wordtext = open('Copy_of_sentence_anaysis_product_edit.txt', 'r', encoding='UTF-8')
    lemmas_sent = []
    counter = 0
    for line in wordtext:
        for word in line.split():
            tokens = word_tokenize(line)  # split words
            tagged_sent = pos_tag(tokens)  # get each word's property
            wnl = WordNetLemmatizer()
            for tag in tagged_sent:
                wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
                word_org = wnl.lemmatize(tag[0], pos=wordnet_pos)
                word_org_new = re.sub('[^a-zA-Z]', '', word_org)
                lemmas_sent.append(word_org_new.lower())  # 词形还原
                lemmas_sent = [i for i in lemmas_sent if i != '']
                for word in lemmas_sent:
                    if word in stop_words:
                        lemmas_sent.remove(word)
            print(lemmas_sent)
            lemmas_sent.sort()
            counter = Counter(lemmas_sent)
            print(counter)
            counter.most_common()
            break
    return lemmas_sent, counter

if __name__ == "__main__":
    trans = file_trans()
    lemmas_sent, counter = clean_word()

    file = open('Copy_of_sentence_anaysis_product_edit_clear.txt', 'w', encoding='UTF-8')
    file.write(str(lemmas_sent))
    file.close()

    file = open('Copy_of_sentence_anaysis_product_edit_counter.txt', 'w', encoding='UTF-8')
    file.write(str(counter))
    file.close()

