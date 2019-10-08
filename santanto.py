from nltk.corpus import wordnet
from vocabulary.vocabulary import Vocabulary as vb
def get_word_synonyms_from_sent(word, sent):
    synonyms = []
    antonyms = []
    for syn in wordnet.synsets("good"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    #if it has to be in the text
    synonyms= list(set(sentence).intersection(syn))
    antonyms = list(set(sentence).intersection(anto))
    return (set(synonyms)),(set(antonyms))
def synset(data):
    result = {}
    syns = wordnet.synsets(data)
    list = []
    for s in syns:
        r = {}
        r["name"] = s.name()
        r["lemma"] = s.lemmas()[0].name()
        r["definition"] = s.definition()
        r["examples"] = s.examples()
        list.append(r)

    result["list"] = list
    synonyms = []
    antonyms = []
    for syn in syns:
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    return synonyms,antonyms

def get_synonyms(word, pos=None):
    wordnet_pos = {
        "NOUN": wordnet.NOUN,
        "VERB": wordnet.VERB,
        "ADJ": wordnet.ADJ,
        "ADV": wordnet.ADV
    }
    if pos:
        synsets = wordnet.synsets(word, pos=wordnet_pos[pos])
    else:
        synsets = wordnet.synsets(word)
    synonyms = []
    for synset in synsets:
        synonyms += [str(lemma.name()) for lemma in synset.lemmas()]
    synonyms = [synonym.replace("_", " ") for synonym in synonyms]
    synonyms = list(set(synonyms))
    synonyms = [synonym for synonym in synonyms if synonym != word]
    return synonyms
def meaning(word):
    syns = wordnet.synsets(word)
    if syns:
        print("WORD WITH ONE MEANING")
        print("DEFINITION OF THIS WORD IS :",syns[0].definition())
    else:
        print("This word has no meaning")

def polysemic_word(word):
    syns = wordnet.synsets(word)
    i = 0
    for s in syns:
        for l in s.lemmas():
            i=i+1
    if i>0:
        print("polysemous word,Nb of usages possible:",i)
        #meaning(word)
    else :
        print("No Polysemy")
        meaning(word)

f=open("output_token.txt", "r")
contents =f.read()
contents=contents.replace("[","")
contents=contents.replace(" ","")
contents=contents.replace("]","")
contents=contents.replace("'","")
contents=contents.replace("\n","")
x=[]
x = list(contents.split(","))
print(x)
for i in x:
    word = None
    sentence = []
    word = str(i)
    sentence = list(contents.split(","))
    sentence.remove(word)
    syn=[]
    anto=[]
    if len(word)>0:
       print("WORD :", word)
       syn,anto=synset(word)
       print("SYNONYMS :", syn, "\nANTONYMS:", anto)
       polysemic_word(word)
       print("__________________________________________________________________________________________________________________________________________________")
    word = None
    sentence = []

