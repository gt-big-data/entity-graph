fullEdges = []
limit = {'$limit': 1000}
for d in db.qdoc.aggregate([limit]):
 wdids = [ent['wdid'] for ent in d['entities'] if ent['wdid'] is not None]
 thisEdges = list(itertools.combinations(wdids, 2))
 fullEdges.extend(thisEdges)
print len(fullEdges)