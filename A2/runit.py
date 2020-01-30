from bs4 import BeautifulSoup as Soup
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
import re
import math
from operator import itemgetter
def getQueries(file):
    print("reading queries ... ")
    queries={}
    handler = open(file).read()
    soup = Soup(handler)
    stemmer = SnowballStemmer('english')
    tknzr = TweetTokenizer()
    stop_list = open('stoplist.txt', 'r').read()
    stop_list = tknzr.tokenize(stop_list)

    for q,i in zip(soup.findAll('query'),soup.findAll('topic')):
        #preprocessing queries

        t_query=tknzr.tokenize(q.getText())

        filtered_query=""
        for word in t_query:
            word=word.lower()
            if word not in stop_list and re.match("^[(a-zA-Z0-9-_')]*$", word) and len(word)>1:
                word = stemmer.stem(word)
                filtered_query=filtered_query+" "+word
        queries[i.attrs['number']]=filtered_query
        filtered_query=""
    return queries

def readTermIndex(indexfile,no_of_docs,no_of_terms):
    print("reading index ... ")
    doclengths=[0]*no_of_docs
    term_data={}

    spacecount=0
    with open(indexfile, 'r') as file:
        for _ in range(no_of_terms):

            spacecount=0
            line=file.readline()
            if line is '':
                break
            termid=line.split()[0]
            for i in range(len(line)-1):

                j=0
                if line[i+1] is '\n':
                    break
                if line[i] is " ":
                    if spacecount is 0:
                        j=i+1
                        x=""
                        while line[j] is not ' ':
                            x=x+line[j]
                            j=j+1
                        term_data[termid]=[int(x),0,dict({})]
                        #term_freq_corpus[int(line[0])]=int(x)
                    if spacecount is 1:
                        j = i + 1
                        x = ""
                        while line[j] is not ' ':
                            x = x + line[j]
                            j = j + 1

                        term_data[termid][1]=int(x)

                        #doc_with_term[int(line[0])] = int(x)
                    if spacecount is 2:
                        i=i+1
                        j=i
                        x=""
                        while line[j] is not ',':
                            x=x+line[j]
                            j=j+1
                        doclengths[int(x)] = doclengths[int(x)] + 1

                        if int(x) not in term_data[termid][2]:
                            term_data[termid][2][int(x)]=1
                        else:
                            term_data[termid][2][int(x)]+=1
                        spacecount=spacecount-1
                    spacecount=spacecount+1

    #   total words in doc
    words_in_corpus=sum(doclengths)
    #   average doc length
    average_doc_length=words_in_corpus/no_of_docs
    return doclengths,term_data,words_in_corpus,average_doc_length

def DirichletSmoothing(docnames,doclengths,term_data,words_in_corpus,average_doc_length,queries,termids):
    print("Dirichlet smoothing ...")
    tknzr = TweetTokenizer()
    list=[]
    mu=no_of_docs/(no_of_docs+average_doc_length)
    mu2=average_doc_length/(no_of_docs+average_doc_length)
    #file=open("drichlet ranking.txt",'w')
    for (qid, query) in queries.items():

        tkquery=tknzr.tokenize(query)
        for i in range(1,no_of_docs):
            name=docnames[str(i)]
            result = 1
            for qword in tkquery:

                if qword in termids:
                    id = termids[qword]
                    #   formula = P1*mu + P2*mu2
                    #   (length_of_doc/length_of_doc+average_doc_length)(tf_in_doc/length_of_doc) + (average_do_length/length_of_doc+average_doc_length)(tf_in_corpus/length_of_corpus)
                    if i in term_data[id][2]:
                        P1=term_data[id][2][i]/doclengths[i]
                    else:
                        P1=0
                    P2=term_data[id][0]/words_in_corpus
                    mu = doclengths[i] / (doclengths[i] + average_doc_length)
                    mu2 = average_doc_length / (doclengths[i] + average_doc_length)
                    result=result*(P1*mu +P2*mu2)

            if result is 1:
                result=0
            a = [qid, name, result, 'run1', '\n']
            list.append(a)

            #file.write(str(qid)+" "+name+ " "+str(i)+" "+str(result)+str(" run1")+'\n')
    return list
def BM25(docnames,doclengths,term_data,words_in_corpus,average_doc_length,queries,termids):
    print("BM25 ...")
    tknzr = TweetTokenizer()
    list=[]
    mu=no_of_docs/(no_of_docs+average_doc_length)
    mu2=average_doc_length/(no_of_docs+average_doc_length)
    rankedlist=[]
    #file=open("BM25.txt",'w')
    for (qid, query) in queries.items():

        tkquery=tknzr.tokenize(query)
        for i in range(1,no_of_docs):
            name=docnames[str(i)]
            result = 0
            for qword in tkquery:

                if qword in termids:
                    id = termids[qword]

                    #   formula

                    D = no_of_docs
                    K = (((doclengths[i]/ average_doc_length) * (0.75)) + (1 - 0.75)) * 1.2
                    parta = float((D + 0.5) / (int(term_data[id][1]) + 0.5))
                    parta = math.log10(parta)
                    if i in term_data[id][2]:
                        partb = float(((1 + 1.2) * term_data[id][2][i]) / (K + term_data[id][2][i]))
                    else:
                        partb = float(((1 + 1.2) * 0) / (K + 0))
                    partc = float(((1 + 10) * tkquery.count(qword)) / (10 + tkquery.count(qword)))

                    result = result + ((parta)*(partb)*(partc))
            a=[qid,name,result,'run1','\n']
            list.append(a)

            #   file.write(str(qid)+" "+name+ " "+str(i)+" "+str(result)+str(" run1")+'\n')
    return list

def getTermIds(file):
    termid_dict={}
    with open(file) as file:
        for line in file:
            key=line.split()[1]
            value=line.split()[0]
            termid_dict[key]=value
    return termid_dict

def getDocnames(file):
    docdict={}
    with open(file) as file:
        for line in file:
            key = line.split()[0]
            value=line.split()[1]
            docdict[key]=value
    return docdict

def rankDocs(list,file):
    print("Ranking docs....")
    file=open(file,'w')
    list.sort(key=itemgetter(2),reverse=True)
    list.sort(key=itemgetter(0))
    rank=1
    for index,line in enumerate(list):
        if line[0] != list[index-1][0]:
            rank=1
        line.insert(2,rank)
        rank=rank+1
        file.write(' '.join(str(v) for v in line))
    return list

def readgrades(file):
    grades_dict = {}
    with open(file) as file:
        for line in file:
            key1 = line.split()[0]
            key2 = line.split()[2]
            score = line.split()[3]
            grades_dict[key1,key2] = score
    return grades_dict

def evaluate(list,gradelist,n,no_of_docs):
    print("Evaluating...")
    dict={}
    notspamdocs=0
    relevant_docs=0
    count=-1
    for index,i in enumerate(list):  #   [qid,name,rank,result,'run1','\n']
        count = count + 1
        if (count) > no_of_docs:
            dict[i[0]] = dict[i[0]] / notspamdocs
            notspamdocs = 0
            relevant_docs = 0
            count=0
            continue

        if (i[0],i[1]) not in gradelist:
            continue
        if gradelist[i[0],i[1]] is '-1': #    spam doc
            continue
        elif gradelist[i[0],i[1]] is '0': #   not relevant
            notspamdocs=notspamdocs+1
        elif gradelist[i[0],i[1]] == '1' or gradelist[i[0],i[1]] == '2' or gradelist[i[0],i[1]] == '3' or gradelist[i[0],i[1]] == '4':  #   relevant
            notspamdocs = notspamdocs + 1
            relevant_docs=relevant_docs+1
            if i[0] in dict :
                dict[i[0]]= dict[i[0]]+(relevant_docs/notspamdocs)
            else:
                dict[i[0]] = (relevant_docs / notspamdocs)

        if n>0 and notspamdocs==n:
            print(relevant_docs/notspamdocs)


    for e in dict:
        print(str(e) +" : "+str(dict[e]))
    return dict


if __name__=="__main__":
    import sys

    print(sys.argv)
    no_of_docs = 3495
    no_of_terms_in_corpus = 158241
    queries = getQueries("topics.xml")
    termids = getTermIds("termids.txt")
    docnames = getDocnames("docids.txt")
    doclengths, term_data, words_in_corpus, average_doc_length = readTermIndex('term_index.txt', no_of_docs,
                                                                               no_of_terms_in_corpus)
    gradelist = readgrades('relevance judgements.qrel')

    if str(sys.argv[1]) == '--score':
        scoring_function = sys.argv[2]
        if scoring_function == "BM25":
            list1 = BM25(docnames, doclengths, term_data, words_in_corpus, average_doc_length, queries, termids)
            list1=rankDocs(list1,'BM25.txt')
            evaluate(list1,gradelist,0,no_of_docs)
            evaluate(list1,gradelist,5,no_of_docs)
            evaluate(list1, gradelist, 10, no_of_docs)
            evaluate(list1, gradelist, 20, no_of_docs)
            evaluate(list1, gradelist, 30, no_of_docs)
        elif scoring_function == "Dirichlet":
            list2 = DirichletSmoothing(docnames, doclengths, term_data, words_in_corpus, average_doc_length, queries,
                                       termids)
            list2 = rankDocs(list2, 'Drichilet smoothin.txt')
            evaluate(list2, gradelist, 0, no_of_docs)
            evaluate(list2, gradelist, 5, no_of_docs)
            evaluate(list2, gradelist, 10, no_of_docs)
            evaluate(list2, gradelist, 20, no_of_docs)
            evaluate(list2, gradelist, 30, no_of_docs)