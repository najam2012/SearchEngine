import glob
import nltk
import re
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from bs4 import BeautifulSoup

tknzr = TweetTokenizer()

all_files = glob.glob('corpus\*')

out = open("outfile.txt", 'w', encoding='UTF-8')
VALID_TAGS = ['div', 'span', 'p', 'center', 'b', 'strong', 'em', 'i', 'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'table', 'td',
              'tr', 'th', 'h1', 'h2', 'h3', 'h4', 'h5']

stop_list = open('stoplist.txt', 'r').read()
stop_list = tknzr.tokenize(stop_list)

# Snowball stemmer is used for stemming
stemmer = SnowballStemmer('english')

for filename in all_files:
    filtered = []
    fileobject = open(filename, 'rb')
    soup = BeautifulSoup(fileobject, 'html.parser')
    for script in soup("script"):
        script.decompose()
    for x in soup.find_all(VALID_TAGS):
        a = tknzr.tokenize(x.get_text())
    for word in a:
        if word not in stop_list:
            if re.match("^[a-zA-Z0-9_]*$", word):
                word = word.lower()
                word = stemmer.stem(word)
                filtered.append(word)
    if filtered:
        out.write(str(filtered))
    fileobject.close()
out.close()
