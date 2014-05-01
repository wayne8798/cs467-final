import json
import csv

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
    hsets[t] = [word for word in doc.lower().split() if word not in stoplist]
    hsets[t] = [word for word in hsets[t] if all(ord(c) < 128 for c in word)]

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
    psets[t] = [word for word in doc.lower().split() if word not in stoplist]
    psets[t] = [word for word in psets[t] if all(ord(c) < 128 for c in word)]

fpris.close()

ffood = open('data/food.txt', 'r')
fsets = {}
for line in ffood.readlines():
    time = int(line.split('\t')[0])
    doc = line.split('\t')[1][:-1]
    if time in fsets.keys():
        fsets[time] += doc
    else:
        fsets[time] = doc

for t in fsets.keys():
    doc = fsets[t]
    fsets[t] = [word for word in doc.lower().split() if word not in stoplist]
    fsets[t] = [word for word in fsets[t] if all(ord(c) < 128 for c in word)]

ffood.close()

obj_dict = {}
fobj = open('data/objective.csv', 'r')
csvreader = csv.reader(fobj, delimiter=',')
for row in csvreader:
    category = row[0]
    year = int(row[1])
    obj = int(row[2])
    sub = int(row[3])
    if not year in obj_dict.keys():
        obj_dict[year] = {}
    obj_dict[year][category] = {}

    total = float(obj + sub)
    if total == 0:
        obj_dict[year][category]['obj'] = 0
        obj_dict[year][category]['sub'] = 0
    else:
        obj_dict[year][category]['obj'] = obj / total
        obj_dict[year][category]['sub'] = sub / total

fobj.close()

json_data = []

for y in range(1950, 2015):
    hls = []
    pls = []
    fls = []
    if y in hsets.keys():
        hls = hsets[y]
    if y in psets.keys():
        pls = psets[y]
    if y in fsets.keys():
        fls = fsets[y]

    hp_overlap = set()
    hf_overlap = set()
    h_uniq = set()
    p_uniq = set()
    f_uniq = set()
    
    for w in hls:
        if w in pls:
            hp_overlap.add(w)            
        if w in fls:
            hf_overlap.add(w)

    for w in hls:
        if not (w in set.union(hp_overlap, hf_overlap)):
            h_uniq.add(w)

    for w in pls:
        if not (w in hp_overlap):
            p_uniq.add(w)

    for w in fls:
        if not (w in hf_overlap):
            f_uniq.add(w)

    dic = {}
    dic['no'] = y

    pol_ls = []
    for w in p_uniq:
        d = {}
        d['f'] = pls.count(w)
        d['w'] = w
        pol_ls.append(d)
    dic['pol'] = {'kw': pol_ls}
    try:
        dic['pol']['sub'] = obj_dict[y]['political']['sub']
        dic['pol']['obj'] = obj_dict[y]['political']['obj']
    except:
        dic['pol']['sub'] = 0
        dic['pol']['obj'] = 0

    foo_ls = []
    for w in f_uniq:
        d = {}
        d['f'] = fls.count(w)
        d['w'] = w
        foo_ls.append(d)
    dic['food'] = {'kw': foo_ls}
    try:
        dic['food']['sub'] = obj_dict[y]['food']['sub']
        dic['food']['obj'] = obj_dict[y]['food']['obj']
    except:
        dic['food']['sub'] = 0
        dic['food']['obj'] = 0

    his_ls = []
    for w in h_uniq:
        d = {}
        d['f'] = hls.count(w)
        d['w'] = w
        his_ls.append(d)
    dic['his'] = {'kw': his_ls}
    try:
        dic['his']['sub'] = obj_dict[y]['history']['sub']
        dic['his']['obj'] = obj_dict[y]['history']['obj']
    except:
        dic['his']['sub'] = 0
        dic['his']['obj'] = 0

    od = {}
    od['pol'] = {'perc': 100 * len(hp_overlap) /
                 (len(p_uniq) + len(h_uniq) + len(hp_overlap) + 1),
                 'kw': list(hp_overlap)}
    od['food'] = {'perc': 100 * len(hf_overlap) /
                  (len(f_uniq) + len(h_uniq) + len(hf_overlap) + 1),
                  'kw': list(hf_overlap)}
    dic['his']['over'] = od

    json_data.append(dic)

fout = open('years.json', 'w')
fout.write(json.dumps(json_data))
fout.close()
