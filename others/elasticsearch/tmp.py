import pymongo
import json
from pymongo import MongoClient
from elasticsearch import Elasticsearch

def get_data():

    col = MongoClient()['scc413']['fact_data']


    result = []
    for item in col.find():
        del item['_id']
        result.append(item)

    f = open('tmp.json', 'w')

    json.dump(result, f, ensure_ascii=False, indent=4)

f = open('tmp.json')
t = json.load(f)
for i in t:
    print(i)
    es = Elasticsearch()
    es.index(index="test-index", body=i)
