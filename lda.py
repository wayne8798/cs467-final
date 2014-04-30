from gensim import corpora, models, similarities

fin = open('data/history.txt', 'r')
documents = fin.readlines()
fin.close()

fstop = open('stopwords.txt', 'r')
stoplist = set(map(lambda x: x[:-1], fstop.readlines()))
fstop.close()

texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.ldamodel.LdaModel(corpus, num_topics=1)
print lda[corpus[0]]

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
