import pandas as pd
import nltk
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

nltk.download('stopwords')
from nltk.corpus import stopwords

print("reading data...")
data_source_url = "Datasets/Question2 Dataset.tsv"
df = pd.read_csv(data_source_url,error_bad_lines=False,delimiter='\t',usecols={'review':str,'sentiment':int})

label=df['sentiment']
text=df['review']
for index,x in enumerate(text):
    soup = BeautifulSoup(text[index],'html.parser')
    text[index]=soup.getText()

print("training...")
X_train, X_test, y_train, y_test = train_test_split(text, label,test_size=0.25, random_state = 0)
count_vect = CountVectorizer(max_features=1500, min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
tf_idf_model = MultinomialNB().fit(X_train_tfidf, y_train)
tf_model=MultinomialNB().fit(X_train_counts, y_train)

print("testing...")
y_predict1=tf_idf_model.predict(count_vect.transform(X_test))
y_predict2=tf_model.predict(count_vect.transform(X_test))

print("accuracy of TF-IDF MODEL:\t" + str(accuracy_score(y_test, y_predict1)))
print("accuracy of TF MODEL:\t" + str(accuracy_score(y_test, y_predict2)))
