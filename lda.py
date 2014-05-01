from gensim import corpora, models, similarities

fhis = open('data/history.txt', 'r')
his_docs = fhis.readlines()
fhis.close()

fpris = open('data/prison.txt', 'r')
pris_docs = fpris.readlines()
fpris.close()

ffood = open('data/food.txt', 'r')
food_docs = ffood.readlines()
ffood.close()

fstop = open('stopwords.txt', 'r')
stoplist = set(map(lambda x: x[:-1], fstop.readlines()))
fstop.close()

documents = his_docs + pris_docs + food_docs

texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

his_texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in his_docs]
pris_texts = [[word for word in document.lower().split() if word not in stoplist]
              for document in pris_docs]
food_texts = [[word for word in document.lower().split() if word not in stoplist]
              for document in food_docs]

all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

his_texts = [[word for word in text if word not in tokens_once]
             for text in his_texts]
pris_texts = [[word for word in text if word not in tokens_once]
              for text in pris_texts]
food_texts = [[word for word in text if word not in tokens_once]
              for text in food_texts]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

food_corpus = [dictionary.doc2bow(text) for text in food_texts]

lda = models.ldamodel.LdaModel(corpus, num_topics=10)

rev_dict = {v:k for k,v in dictionary.token2id.items()}
topics = lda.show_topics(topn=20, formatted=False)
t_count = 1
for t in topics:
    print 'Topic %d' % t_count
    t_count += 1
    for pair in t:
        weight = pair[0]
        word = rev_dict[int(pair[1])]
        print word + ': ' + str(weight)
    print '==========================='

for text in food_corpus:
    print lda[text]
