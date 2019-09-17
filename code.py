import glob
import nltk
import re
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from bs4 import BeautifulSoup
import os

def printInvertedHash(hashtable):
    with open("term_index.txt", 'w') as invindex:
        invindex.seek(0)
        invindex.truncate()
        for (key,value) in hashtable.items():
            invindex.write(str(value[0])+"\t"+str(value[1])+"\t"+str(len(value[2]))+"\t")
            for (k,v) in value[2].items():
                for x in v:
                    invindex.write(str(k) + " , "+str(x) +"\t")
            invindex.write("\n")


def createInvertedIndex_Hastable():
    invertedhash = {}
    dochash={}
    count_term_ids = 0
    count_term_ids2 = 0
    count_doc_ids = 0
    try:
        tknzr = TweetTokenizer()
        all_files = glob.glob('corpus\*')       # to access directory
        stop_list = open('stoplist.txt', 'r').read()
        stop_list = tknzr.tokenize(stop_list)

        stemmer = SnowballStemmer('english')           # Snowball stemmer is used for stemming
        for filename in all_files:
            word_position=0

            with open ("docids.txt",'a') as docids :
                docids.write(str(count_doc_ids)+'\t'+filename[7:]+'\n')
            dochash[count_doc_ids]=filename
            count_doc_ids=count_doc_ids+1

            with open(filename, 'rb') as fileobject :
                soup = BeautifulSoup(fileobject, 'html.parser',from_encoding="iso-8859-1")
                for x in soup.find_all('body'):     # taking the <body/> tag
                    all_words=[]
                    for word in tknzr.tokenize(x.get_text(" ")):
                        word_position+=1
                        word = word.lower()         # to lower case
                        if word not in stop_list and re.match("^[(a-zA-Z0-9-_')]*$", word) and len(word)>1:     # using regex equation for filtering special character words
                        #^[a-zA-Z0-9]+((['][_][-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$
                            word = stemmer.stem(word)       # snowball for stemming
                            if not word in invertedhash:
                                invertedhash[word] = [count_term_ids2, 1,dict({})]
                                invertedhash[word][2][count_doc_ids] = [word_position]

                                word_position=word_position+1
                                all_words.append(word)
                                count_term_ids2=count_term_ids2+1
                            else:
                                invertedhash[word][1]=invertedhash[word][1]+1
                                if count_doc_ids in invertedhash[word][2]:
                                    invertedhash[word][2][count_doc_ids].append(word_position)
                                else:
                                    invertedhash[word][2][count_doc_ids]=[word_position]
                                word_position = word_position + 1
                    with open("termids.txt", 'a') as termids:
                        for w in all_words:
                            termids.write(str(str(count_term_ids) + '\t' + w + '\n'))
                            count_term_ids = count_term_ids + 1
    except IOError:
       print(IOError)
    return invertedhash,dochash

def createInverted_BySorting():
    termhash = {}
    count_term_ids = 0
    count_term_ids2 = 0
    count_doc_ids = 0
    IndexList=[]
    try:
        tknzr = TweetTokenizer()
        all_files = glob.glob('corpus\*')       # to access directory
        stop_list = open('stoplist.txt', 'r').read()
        stop_list = tknzr.tokenize(stop_list)

        stemmer = SnowballStemmer('english')           # Snowball stemmer is used for stemming
        for filename in all_files:
            word_position=0

            with open ("docids.txt",'a') as docids :
                docids.write(str(count_doc_ids)+'\t'+filename[7:]+'\n')
            count_doc_ids=count_doc_ids+1

            with open(filename, 'rb') as fileobject :
                soup = BeautifulSoup(fileobject, 'html.parser',from_encoding="iso-8859-1")
                for x in soup.find_all('body'):     # taking the <body/> tag
                    all_words=[]
                    for word in tknzr.tokenize(x.get_text(" ")):
                        word_position+=1
                        word = word.lower()         # to lower case
                        if word not in stop_list and re.match("^[(a-zA-Z0-9-_')]*$", word) and len(word)>1:     # using regex equation for filtering special character words
                        #^[a-zA-Z0-9]+((['][_][-][a-zA-Z0-9])?[a-zA-Z0-9]*)*$
                            word = stemmer.stem(word)       # snowball for stemming
                            if not word in termhash:
                                termhash[word] = [count_term_ids2]
                                IndexList.append((count_doc_ids,count_term_ids2,word_position))
                                #invertedhash[word][2][word_position] = count_doc_ids
                                word_position=word_position+1
                                all_words.append(word)
                                count_term_ids2=count_term_ids2+1
                            else:
                                #invertedhash[word][1]=invertedhash[word][1]+1
                                #invertedhash[word][2][word_position]=count_doc_ids

                                IndexList.append((count_doc_ids, termhash[word][0], word_position))
                                word_position = word_position + 1
                    with open("termids.txt", 'a') as termids:
                        for w in all_words:
                            termids.write(str(str(count_term_ids) + '\t' + w + '\n'))
                            count_term_ids = count_term_ids + 1
    except IOError:
       print(IOError)
    return IndexList


def printSortedIndex(SortedIndex):      #(docid,termid,position)
    word_count = 0
    indoc = 0
    i = -1
    j = -1
    doclist = []
    termlist=""

    SortedIndex.sort(key=lambda tup: tup[1])
    with open("term_index.txt", 'w') as indexfile:
        indexfile.seek(0)
        indexfile.truncate()

        for tup in SortedIndex:
            if tup[1] is not i:

                if i is not -1:
                    indexfile.write("\n" + str(tup[1]-1) + "\t")
                    indexfile.write(str(word_count) + "\t" + str(len(doclist))+"\t")
                    indexfile.write(termlist)
                doclist.clear()
                termlist=""
                word_count=0
            else:
                word_count=word_count+1
                termlist+=str(str(tup[0])+","+str(tup[2])+"\t")
            if tup[0] is not j:
                doclist.append(tup)


            i = tup[1]
            j = tup[0]

def read(invertedHashtable,dochash,term):
        stemmer = SnowballStemmer('english')
        term=stemmer.stem(term)

        if not term in invertedHashtable:
            print(" Term not found ")
        else:
            print("Listing for term : "+term)
            print( "Termid : "+str(invertedHashtable[term][0]))
            print("Number of documents containing term: "+str(len(invertedHashtable[term][2])))
            print("Term frequency in corpus: "+str(invertedHashtable[term][1]))
            #for key in invertedHashtable[term][2].keys():
             #   print(dochash[key])

if __name__ == "__main__":
    import sys
    if str(sys.argv[1][2:]) == 'term':
        term=sys.argv[2]
        #printInvertedHash(createInvertedIndex_Hastable())
        #printSortedIndex(createInverted_BySorting())
        print("Indexing....")
        x,y=createInvertedIndex_Hastable()
        printInvertedHash(x)
        read(x,y,term)