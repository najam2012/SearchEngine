import gensim

def read(file):
    with open(file, 'rb') as f:
        for i, line in enumerate(f):
            yield gensim.utils.simple_preprocess(line)

documents = list(read('Datasets/Question1.txt'))
model = gensim.models.Word2Vec (documents, size=125, window=5, min_count=2, workers=8)
model.train(documents,total_examples=len(documents),epochs=1)

#   testing
print(model.wv.most_similar (positive='Clean'.lower()))
print(model.wv.most_similar (positive='Unclean'.lower()))
print(model.wv.most_similar (positive='Amazed'.lower()))
print(model.wv.most_similar (positive='friendly'.lower()))

