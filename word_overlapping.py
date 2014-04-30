fstop = open('stopwords.txt', 'r')
stoplist = set(map(lambda x: x[:-1], fstop.readlines()))
fstop.close()

fhist = open('data/history.txt', 'r')
hsets = {}
for line in fhist.readlines():
    time = int(line.split('\t')[0])
    doc = line.split('\t')[1][:-1]
    if time in hsets.keys():
        hsets[time] += doc
    else:
        hsets[time] = doc

for t in hsets.keys():
    doc = hsets[t]
    hsets[t] = set(word for word in doc.lower().split() if word not in stoplist)

print hsets
fhist.close()

fpris = open('data/prison.txt', 'r')
psets = {}
for line in fpris.readlines():
    time = int(line.split('\t')[0])
    doc = line.split('\t')[1][:-1]
    if time in psets.keys():
        psets[time] += doc
    else:
        psets[time] = doc

for t in psets.keys():
    doc = psets[t]
    psets[t] = set(word for word in doc.lower().split() if word not in stoplist)

print psets
fpris.close()

for y in range(1950, 2015):
#for ys in [1950, 1955, 1960, 1965, 1970, 1975, 1980,
#           1985, 1990, 1995, 2000, 2005, 2000]:
    hset = set()
    pset = set()
    if not (y in hsets.keys() and y in psets.keys()):
        continue
    hset = set.union(hset, hsets[y])
    pset = set.union(pset, psets[y])
    overlap_count = 0
    overlap_set = set()
    for w in hset:
        if w in pset:
            overlap_set.add(w)
            overlap_count += 1
    print y
    print 'history: %d' % len(hset)
    print 'prison: %d' % len(pset)
    print overlap_set
    print float(overlap_count) / len(set.union(hset, pset))
