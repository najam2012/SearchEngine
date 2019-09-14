import glob
import nltk
import re
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from bs4 import BeautifulSoup
import os

tknzr = TweetTokenizer()

all_files = glob.glob('corpus\*')

stop_list = open('stoplist.txt', 'r').read()
stop_list = tknzr.tokenize(stop_list)

#termids=open("termids.txt",'w',encoding='UTF-8')
#docids=open ("docids.txt",'w',encoding='UTF-8')

#term_index=open('term_index.txt','w',encoding='UTF=8')

VALID_TAGS = ['div','span', 'p', 'a','center', 'b', 'strong', 'em', 'i',  'li', 'dt', 'dd', 'td',
             'th', 'h1', 'h2', 'h3', 'h4', 'h5']


# Snowball stemmer is used for stemming
stemmer = SnowballStemmer('english')

invertedhash={}
termidhash={}
count_term_ids=0
count_term_ids2=0
count_doc_ids=0

for filename in all_files:
    word_position=0
    with open ("docids.txt",'a') as docids :
        docids.write(str(str(count_doc_ids)+'\t'+filename[7:]+'\n'))
    count_doc_ids=count_term_ids+1
    try:
        with open(filename, 'rb') as fileobject :
            soup = BeautifulSoup(fileobject, 'html.parser')
            for x in soup.find_all('body'):
                all_words=[]
                for word in tknzr.tokenize(x.get_text(" ")):
                    word_position+=1
                    word = word.lower()
                    if word not in stop_list and re.match("^[(a-zA-Z0-9-_')]*$", word) and len(word)>1:
                        #^[a-zA-Z0-9]+((['][_][-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$
                        word = stemmer.stem(word)
                        if not word in termidhash:
                            termidhash[word]=count_term_ids2
                            invertedhash[word] = [count_term_ids2, +1, 0,{count_doc_ids,word_position}]
                            word_position+=1
                            all_words.append(word)
                            count_term_ids2=count_term_ids2+1
                        else:
                            invertedhash[word][1]+=1

                with open("termids.txt", 'a') as termids:
                    for w in all_words:
                        termids.write(str(str(count_term_ids) + '\t' + w + '\n'))
                        count_term_ids = count_term_ids + 1

    except IOError:
        print(IOError)

#docids.close()
#termids.close()
#term_index.close()
