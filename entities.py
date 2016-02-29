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

    unwind = {"$unwind": '$entities'}
    lookup = {
            "$lookup":
            {
                "from": "entities",
                "localField": "entities.text",
                "foreignField": "title",
                "as": "entity_lookup"
            }
    }
    match = {"$match": {"entity_lookup.type" : "human"}}
    limit = {"$limit": 25}
    project = {"$project": { "_id" : 1, "entities" : 1, "title" : 1 } }
    result = db.qdoc.aggregate([limit, project, unwind, lookup, match])

    output_file = open("humans.txt", "w")

    #Error found: _id can't be trusted in qdoc, text can probably

    titleLookup = {}
    for item in result:
        print(item)
        articleTitle = item['title']
        entityTitle = item['entity_lookup'][0]['title']

        if (articleTitle not in titleLookup):
            titleLookup[articleTitle] = set()

        titleLookup[articleTitle].add(entityTitle)
    
    adjMatrix = {}

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

    graphInput = {"nodes" : [], "links" : []}
    print(adjMatrix)
    for source, otherEntities in adjMatrix.items():
        graphInput['nodes'].append({"name" : source, "group" : 0})
        for target in otherEntities:
            graphInput['links'].append({"source" : idLookup[source], "target" : idLookup[target], "value" : adjMatrix[source][target]})
    #print('graph' + str(graphInput))
    output_file.close()

    with open('entities.json', 'w') as fp:
        json.dump(graphInput, fp)

qdocEntityLookup()
#testing()