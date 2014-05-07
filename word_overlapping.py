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
    doc = ' '.join(doc.split('.'))
    doc = ' '.join(doc.split(','))
    if time in hsets.keys():
        hsets[time] += doc
    else:
        hsets[time] = doc

for t in hsets.keys():
    doc = hsets[t]
    hsets[t] = [word for word in doc.lower().split() if word not in stoplist]
    hsets[t] = [word for word in hsets[t] if all(ord(c) < 128 for c in word)]
    hsets[t] = [word for word in hsets[t]
                if not all(ord(c) < 58 and ord(c) > 47 for c in word)]

fhist.close()

fpris = open('data/prison.txt', 'r')
psets = {}
for line in fpris.readlines():
    time = int(line.split('\t')[0])
    doc = line.split('\t')[1][:-1]
    doc = ' '.join(doc.split('.'))
    doc = ' '.join(doc.split(','))
    if time in psets.keys():
        psets[time] += doc
    else:
        psets[time] = doc

for t in psets.keys():
    doc = psets[t]
    psets[t] = [word for word in doc.lower().split() if word not in stoplist]
    psets[t] = [word for word in psets[t] if all(ord(c) < 128 for c in word)]
    psets[t] = [word for word in psets[t]
                if not all(ord(c) < 58 and ord(c) > 47 for c in word)]

fpris.close()

ffood = open('data/food.txt', 'r')
fsets = {}
for line in ffood.readlines():
    time = int(line.split('\t')[0])
    doc = line.split('\t')[1][:-1]
    doc = ' '.join(doc.split('.'))
    doc = ' '.join(doc.split(','))
    if time in fsets.keys():
        fsets[time] += doc
    else:
        fsets[time] = doc

for t in fsets.keys():
    doc = fsets[t]
    fsets[t] = [word for word in doc.lower().split() if word not in stoplist]
    fsets[t] = [word for word in fsets[t] if all(ord(c) < 128 for c in word)]
    fsets[t] = [word for word in fsets[t]
                if not all(ord(c) < 58 and ord(c) > 47 for c in word)]
ffood.close()

farticles = open('data/articles.csv', 'r')
asets = {}
for line in farticles.readlines():
    time = int(line.split(',')[0])
    doc = ' '.join(line.split(',')[1:])
    clean_doc = ''
    for c in doc:
        if not c in [',', '.', '[', ']', '(', ')', '-']:
            clean_doc += c
    doc = clean_doc
    if time in asets.keys():
        asets[time] += doc
    else:
        asets[time] = doc

for t in asets.keys():
    doc = asets[t]
    asets[t] = [word for word in doc.lower().split() if word not in stoplist]
    asets[t] = [word for word in asets[t] if all(ord(c) < 128 for c in word)]
    asets[t] = [word for word in asets[t]
                if not all(ord(c) < 58 and ord(c) > 47 for c in word)]

farticles.close()

obj_dict = {}
overall_obj_dict = {}

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

    if not category in overall_obj_dict.keys():
        overall_obj_dict[category] = {}
        overall_obj_dict[category]['obj'] = obj
        overall_obj_dict[category]['sub'] = sub
    else:
        overall_obj_dict[category]['obj'] += obj
        overall_obj_dict[category]['sub'] += sub        

fobj.close()

faobj = open('data/objectiveArticle.csv', 'r')
csvreader = csv.reader(faobj, delimiter=',')
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
overall_hset = set()
overall_pset = set()
overall_fset = set()
overall_aset = set()

for y in range(1950, 2015):
    hls = []
    pls = []
    fls = []
    als = []

    if y in hsets.keys():
        hls = hsets[y]
    if y in psets.keys():
        pls = psets[y]
    if y in fsets.keys():
        fls = fsets[y]
    if y in asets.keys():
        als = asets[y]

    overall_hset = set.union(overall_hset, set(hls))
    overall_pset = set.union(overall_pset, set(pls))
    overall_fset = set.union(overall_fset, set(fls))
    overall_aset = set.union(overall_aset, set(als))

    hp_overlap = set()
    hf_overlap = set()
    h_uniq = set()
    p_uniq = set()
    f_uniq = set()

    ap_overlap = set()
    ah_overlap = set()
    af_overlap = set()
    a_uniq = set()
    
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

    for w in als:
        if w in hls or w in pls or w in fls:
            if w in hls:
                ah_overlap.add(w)
            if w in pls:
                ap_overlap.add(w)
            if w in fls:
                af_overlap.add(w)
        else:
            a_uniq.add(w)

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

    nd = {}
    ahis_ls = []
    for w in ah_overlap:
        d = {}
        d['f'] = hls.count(w)
        d['w'] = w
        ahis_ls.append(d)
    nd['his'] = {'kw': ahis_ls}

    afoo_ls = []
    for w in af_overlap:
        d = {}
        d['f'] = fls.count(w)
        d['w'] = w
        afoo_ls.append(d)
    nd['food'] = {'kw': afoo_ls}

    apol_ls = []
    for w in ap_overlap:
        d = {}
        d['f'] = pls.count(w)
        d['w'] = w
        apol_ls.append(d)
    nd['pol'] = {'kw': apol_ls}

    auniq_ls = []
    for w in a_uniq:
        d = {}
        d['f'] = als.count(w)
        d['w'] = w
        auniq_ls.append(d)
    nd['no_over'] = {'kw': auniq_ls}
    nd['sub'] = obj_dict[y]['articles']['sub']
    nd['obj'] = obj_dict[y]['articles']['obj']
    
    dic['news'] = nd

    json_data.append(dic)

overall_data = {}
hp_overlap = set()
hf_overlap = set()
for w in overall_hset:
    if w in overall_pset:
        hp_overlap.add(w)
    if w in overall_fset:
        hf_overlap.add(w)

ap_overlap = set()
ah_overlap = set()
af_overlap = set()
for w in overall_aset:
    if w in overall_pset:
        ap_overlap.add(w)
    if w in overall_hset:
        ah_overlap.add(w)
    if w in overall_fset:
        af_overlap.add(w)

pol_dic = {}
pol_total = float(overall_obj_dict['political']['obj'] +
                  overall_obj_dict['political']['sub'])
pol_dic['sub'] = overall_obj_dict['political']['sub'] / pol_total
pol_dic['obj'] = overall_obj_dict['political']['obj'] / pol_total
pol_len = float(len(overall_pset))
pol_dic['his'] = len(hp_overlap) / pol_len
pol_dic['media'] = len(ap_overlap) / pol_len
overall_data['pol'] = pol_dic

his_dic = {}
his_total = float(overall_obj_dict['history']['obj'] +
                  overall_obj_dict['history']['sub'])
his_dic['sub'] = overall_obj_dict['history']['sub'] / his_total
his_dic['obj'] = overall_obj_dict['history']['obj'] / his_total
his_len = float(len(overall_hset))
his_dic['pol'] = len(hp_overlap) / his_len
his_dic['food'] = len(hf_overlap) / his_len
his_dic['media'] = len(ah_overlap) / his_len
overall_data['his'] = his_dic
    
food_dic = {}
food_total = float(overall_obj_dict['food']['obj'] +
                   overall_obj_dict['food']['sub'])
food_dic['sub'] = overall_obj_dict['food']['sub'] / food_total
food_dic['obj'] = overall_obj_dict['food']['obj'] / food_total
food_len = float(len(overall_fset))
food_dic['his'] = len(hf_overlap) / food_len
food_dic['media'] = len(af_overlap) / food_len
overall_data['food'] = food_dic

fout = open('years.json', 'w')
fout.write(json.dumps(json_data))
fout.close()

fout = open('overall.json', 'w')
fout.write(json.dumps(overall_data))
fout.close()
