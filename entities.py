from dbco import *
import pprint
import json

def testing():

    db.qdoc.find().count
    #print(db.entities.find_one())
    db.qdoc.find().limit(1).skip(1000)
    art = list(db.qdoc.find({'entities': {'$exists': True}}).limit(1).skip(10000))[0]
    print('artobject' + str(art))
    '''
    for entity in art['entities']:
        print entity
    '''
    #print(list(db.entities.find({'_id': 'Q1'})))
    #P31


#Adds the type field to all entities
def addHumanType():
    #numeric-id is "human" (Q5)
    #_id is what the entity actually is
    #wdid refers to "Instance of"
    humanCount = 0
    entityLookup = list(db.entities.find({'_id': {'$exists': True}}).limit(100))
    for entity in entityLookup:
        #print(entity)
        properties = entity['properties']
        if ('Instance of' in properties.keys()):
            if (properties['Instance of']['value']['numeric-id'] == 5):
                humanCount += 1
                #print(entity['_id'])
                print(entity)
                #Do the actual update
                #db.entities.update( { "_id": entity['_id'] },{"$set": {"type": 'human' }})
    print('found ' + str(humanCount) + ' humans')

def qdocEntityLookup():
    
    '''
    wdoc = db.qdoc
    article = wdoc.find_one()
    #pprint.pprint(article)
    for entity in article['entities']:
        print(entity)
        break

    entities = db.entities
    entity = entities.find_one()
    #pprint.pprint(article)
    print(entity)
    '''
    
    import pymongo
    '''
    import itertools

    fullEdges = []
    limit = {'$limit': 10}
    for d in db.qdoc.aggregate([limit]):
        #   print(d['entities'])
        wdids = [ent['wdid'] for ent in d['entities'] if ent['wdid'] is not None]
        thisEdges = list(itertools.combinations(wdids, 2))
        fullEdges.extend(thisEdges)
    print fullEdges
    return
    '''

    ARTICLE_LIMIT = 10000
    HUMANS_LIMIT = 1500

    limit = {"$limit": ARTICLE_LIMIT}
    project = {"$project": { "_id" : 1, "entities" : 1, "title" : 1 } }
    unwind = {"$unwind": '$entities'}
    lookup = {
            "$lookup":
            {
                "from": "entities",
                "localField": "entities.wdid",
                "foreignField": "_id",
                "as": "entity_lookup"
            }
    }
    fakeUnwind = {"$unwind": '$entity_lookup'}
    match = {"$match": {"entity_lookup.type" : "human"}}
    group = {'$group': {'_id': '$entities.wdid', 'articleids' : {'$push': '$_id'}, 'title': {'$first': '$entity_lookup.title'}, 'count': {'$sum': 1}}}
    sort = {'$sort': {'count': -1}}
    humansLimit = {'$limit': HUMANS_LIMIT}
    print("Fetching articles with aggregation...")
    results = list(db.qdoc.aggregate([limit, project, unwind, lookup, fakeUnwind, match, group, sort, humansLimit]))
    print("Aggregation complete")

    graphInput = {"nodes" : [], "links" : []}

    numberID = 0
    for entry in results:
        print(entry['count'], entry['title'])
        graphInput['nodes'].append({"name" : entry['title'], "group" : 0})
        entry['numberID'] = numberID
        entry['articleids'] = set([str(x) for x in entry['articleids']])
        numberID += 1

    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            numEdges = len(results[i]['articleids'] & results[j]['articleids'])
            #print(numEdges)
            if (int(numEdges) > 3):
                graphInput['links'].append({"source" : results[i]['numberID'], "target" : results[j]['numberID'], "value" : numEdges})

    with open('entities.json', 'w') as fp:
        json.dump(graphInput, fp)

    '''    
    return
    output_file = open("humans.txt", "w")

    #Error found: _id can't be trusted in qdoc, text can probably

    titleLookup = {}
    for item in result:
        #print(item)
        articleTitle = item['title']
        entityTitle = item['entity_lookup'][0]['title']

        if (articleTitle not in titleLookup):
            titleLookup[articleTitle] = set()

        titleLookup[articleTitle].add(entityTitle)

    print("Processed all articles")
    
    print("Constructing adjacency matrix")
    adjMatrix = {}

    personCount = {}

    for title, people in titleLookup.items():

        for person in people:
            if (person not in adjMatrix):
                adjMatrix[person] = {}
            for subPerson in people:
                if (subPerson != person):
                    if (subPerson not in adjMatrix[person]):
                        adjMatrix[person][subPerson] = 1
                    else:
                        adjMatrix[person][subPerson] = adjMatrix[person][subPerson] + 1



    output_file.write(json.dumps(adjMatrix, encoding="utf-8") + '\n')
    #match = {"$match": {"timestamp" : {"$gt" : startTime, "$lt" : endTime}}}
    #qdocLookup = list(db.qdoc.find({'_id': {'$exists': True}}).limit(100))

    idLookup = {}
    for id, entry in enumerate(adjMatrix.keys()):
        idLookup[entry] = id
    #print('id' + str(idLookup))

    print("Constructing d3 JSON")
    graphInput = {"nodes" : [], "links" : []}
    #print(adjMatrix)
    for source, otherEntities in adjMatrix.items():
        graphInput['nodes'].append({"name" : source, "group" : 0})
        for target in otherEntities:
            graphInput['links'].append({"source" : idLookup[source], "target" : idLookup[target], "value" : adjMatrix[source][target]})
    output_file.close()

    with open('entities.json', 'w') as fp:
        json.dump(graphInput, fp)
    '''
qdocEntityLookup()
#testing()

'''
print("Constructing d3 JSON")
    graphInput = {"nodes" : [], "links" : []}
    #print(adjMatrix)
    for source, otherEntities in adjMatrix.items():
        added = False
        for target in otherEntities:
            if (adjMatrix[source][target] > 2):
                if (not added):
                    graphInput['nodes'].append({"name" : source, "group" : 0})
                    added = True
                graphInput['links'].append({"source" : idLookup[source], "target" : idLookup[target], "value" : adjMatrix[source][target]})
    print('graph' + str(graphInput))
    output_file.close()
'''