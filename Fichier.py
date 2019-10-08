# coding=utf-8
#Extraction du texte à partir des fichiers HTML
import re, string, unicodedata
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
fname="/home/katia/Téléchargements/delicioust140_documents/fdocuments/0a/0a0af4e6f3139e18100f13f7fe6c8f4b.html"
print("Ouverture et lecture du document")
HtmlFile = open(fname, 'r')
print("lecture du fichier html:")
source_code = HtmlFile.read()
print("Retirer les balises HTML :")
VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br','title','h1','tag']

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
    return re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))*[\r\n]*', '', text, flags=re.MULTILINE)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

sample = denoise_text(document)
def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)

sample = replace_contractions(sample)
print("_____________________Normalisation et tokenization du texte avec SPACY____________________")

import spacy
from spacy.lang.en import English
parser = English()

def tokenize(text):
    lda_tokens = []
    text = denoise_text(text)
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
#fin de la normalisation
#lemmatisation et stemming
from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
#Importer la liste des stop words anglais de NLTK
from nltk.stem.wordnet import WordNetLemmatizer
en_stop = set(nltk.corpus.stopwords.words('english'))
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)
#fonction qui regroupe toutes les opérations
def prepare_text(text):
    tokens = tokenize(text) #tokenization
    tokens = [token for token in tokens if len(token) > 4] #avoir les mots dont la longueur depasse 4 caractéres
    tokens = [token for token in tokens if token not in en_stop] #retirer les stop words
    tokens = [get_lemma(token) for token in tokens] #lemmatisation des resultats
    return tokens

#mettre le resultat dans un fichier texte
import codecs
d= codecs.open("output.txt", "w+", "utf-8")
d.write(document)
d.close()
#Ouverture du fichier texte pour un prétraitement
d= codecs.open("output_token.txt", "w+", "utf-8")
import random
text_data = []
with codecs.open("output.txt", "r", "utf-8") as f:
    for line in f:
        if line == '\n':
            line.strip()
        else:
            tokens = prepare_text(line)
            #print(tokens,'\n')
            text_data.append(tokens)
d.write(str(text_data))
d.close()

#Tfd-idf vectorizer
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
corpus = codecs.open("output_token.txt", "r", "utf-8")
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names())
print(X.toarray())
