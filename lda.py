from gensim import corpora, models, similarities

fin = open('data/test.txt', 'r')
documents = fin.readlines()
fin.close()

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.ldamodel.LdaModel(corpus, num_topics=3)

print dictionary.token2id
print lda.show_topics()

