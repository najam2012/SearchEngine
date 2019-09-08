import glob
import nltk
import re
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from bs4 import BeautifulSoup

tknzr = TweetTokenizer()

all_files = glob.glob('corpus\*')

stop_list = open('stoplist.txt', 'r').read()
stop_list = tknzr.tokenize(stop_list)

#termids=open("termids.txt",'w',encoding='UTF-8')
#docids=open ("docids.txt",'w',encoding='UTF-8')

#term_index=open('term_index.txt','w',encoding='UTF=8')

VALID_TAGS = ['div', 'span', 'p', 'a','center', 'b', 'strong', 'em', 'i', 'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'table', 'td',
              'tr', 'th', 'h1', 'h2', 'h3', 'h4', 'h5']


# Snowball stemmer is used for stemming
stemmer = SnowballStemmer('english')

termidhash={}
count_term_ids=0
count_doc_ids=0

for filename in all_files:
    with open ("docids.txt",'a') as docids :
        docids.write(str(str(count_doc_ids)+'\t'+filename+'\n'))
    count_doc_ids=count_doc_ids+1
    try:
        with open(filename, 'rb') as fileobject :
            soup = BeautifulSoup(fileobject, 'html.parser')
            for x in soup.find_all(VALID_TAGS):
                a=tknzr.tokenize(x.get_text())
                for word in a:
                    word = word.lower()
                    if word not in stop_list and re.match("^[a-zA-Z0-9]+((['][_][-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$", word) and len(word)>1:
                        #word = stemmer.stem(word)
                        if not word in termidhash:
                            termidhash[word] = count_term_ids
                            count_term_ids = count_term_ids + 1
                            with open("termids.txt", 'a') as termids :
                                termids.write(str(str(count_term_ids)+'\t'+ word +'\n'))
    except IOError:
        print(IOError)

docids.close()
termids.close()
#term_index.close()
