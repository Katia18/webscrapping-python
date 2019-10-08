# coding=utf-8
import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
#fname="/home/katia/Téléchargements/delicioust140_documents/fdocuments/00/00a2a06e29030e462ee49d47ce1f940c.html"
fname="/home/katia/Téléchargements/delicioust140_documents/fdocuments/e1/e1a046c86f53a11f01e9a1291fe03dc2.html"
print("Ouverture et lecture du document")
HtmlFile = open(fname, 'r')
print("lecture du fichier html:")
source_code = HtmlFile.read() 
print("Retirer les balises HTML :")

from bs4 import BeautifulSoup

VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br','title','h1']

def sanitize_html(value):

    soup = BeautifulSoup(value,features="html.parser")

    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True

    return soup.renderContents()


html=sanitize_html(source_code)
soup = BeautifulSoup(html,features="html.parser")
title = soup.find('title').get_text()
document = ' '.join([p.get_text() for p in soup.find_all('p')])
#cleaning 

page = soup.getText()
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()
def remove_between_square_brackets(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

sample = denoise_text(document)
def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)

sample = replace_contractions(sample)
#print(sample)
'''
print("_____________________Normalisation et tokenization du texte avec NLTK____________________")
#minuscule 
sample = sample.lower()
#  Tokens
words = nltk.word_tokenize(sample)
def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    return words

words = normalize(words)
print("nombre total de tokens dans le document :",len(words))

#Stem et lemmatization 
def stem_and_lemmatize(words):
    stems = stem_words(words)
    lemmas = lemmatize_verbs(words)
    return stems, lemmas

stems, lemmas = stem_and_lemmatize(words)
'''
print("_____________________Normalisation et tokenization du texte avec SPACY____________________")

import spacy
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    toke = parser(text)
    for token in toke:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens
print("nombre total de tokens dans le document :",len(tokenize(document)))

#lemmatisation et stemming 
from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
from nltk.stem.wordnet import WordNetLemmatizer
en_stop = set(nltk.corpus.stopwords.words('english'))
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)
def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens
import codecs
d= codecs.open("output.txt", "w", "utf-8")
d.write(document)
d.close()
import random
text_data = []
with codecs.open("output.txt", "r", "utf-8") as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        print(tokens,'\n')
        text_data.append(tokens)

from gensim.corpora import Dictionary

dictionary  = Dictionary(text_data)

corpus = [dictionary.doc2bow(text) for text in text_data]

import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')
import gensim
NUM_TOPICS = 4
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)
dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')

import pyLDAvis.gensim
lda3 = gensim.models.ldamodel.LdaModel.load('model3.gensim')
lda_display3 = pyLDAvis.gensim.prepare(lda3, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display3)
