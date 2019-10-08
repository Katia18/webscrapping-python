# coding=utf-8
import nltk
from gensim.summarization import summarize,keywords
# getting text document from file
fname="/home/katia/PycharmProjects/Projet/output.txt"
with open(fname, 'r') as myfile:
      text=myfile.read()
#_________________________________ SUMMARY_________________________________
print ('Summary:')
print (summarize(text,word_count=50))
print("_________________________________________________________________________")
#----------------------------------- KEYWORDS -------------------------------
keys = keywords(text).split('\n')
print("Keywords of this file are : \n",keys)
#------------------------------------------------------------------------------
Class= ['Office', 'School', 'phone', 'Technology', 'Electronics', 'Cell', 'Business', 'Education', 'Classroom']
programming=['programming','linux','disassembly','folder','memory','application','debug','java','python','#C','c++','computer','compiler','computers','IDE','language',]
music=["pop","sing","singer","producer","CD","MP3","rock","jazz","blues"]
web=["internet","website","informations","www","link"]
culture=['culture','cultural','feminist','books','letter','magazines','articles','travel','smart','nature','science']
education= ["education","school","college","degree","exams","test","homework","learn","learning"]
design=["design","logo","creative","draw","visual","graphic"]
health = ["heart","doctor",""]
transport = ["cars","toyota","wheels","wheel"]
food = ["food","restraunt","cook","cooking","vegetables","fruits","pizza","cheese"]

if bool(set(keys) & set(culture)) :
    print("Subject of the text : Culture")
if bool(set(keys) & set(web)) :
    print("Subject of the text : Web")
if bool(set(keys) & set(education)) :
    print("Subject of the text : Education")
if bool(set(keys) & set(music)) :
    print("Subject of the text : Music")
if bool(set(keys) & set(programming)) :
    print("Subject of the text : Programming ")
if bool(set(keys) & set(design)) :
    print("Subject of the text : Design")
if bool(set(keys) & set(Class)) :
    print("Subject of the text : school")
if bool(set(keys) & set(transport)) :
    print("Subject of the text : Transports")
if bool(set(keys) & set(food)) :
    print("Subject of the text : Food")
if bool(set(keys) & set(health)) :
    print("Subject of the text : Health")
