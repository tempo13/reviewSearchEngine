from typing import Optional
from fastapi import FastAPI
from create_es_query import CreateEsIndex
import uvicorn

import json
import elasticsearch

app = FastAPI()
f = open('config.json')
config = json.loads(f.read())
es = elasticsearch.Elasticsearch([f"http://{config['host_url']}:9200"], http_auth=(config['username'], config['password']))


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/search/keyword")
def search_result(search: str = None):
    qry = CreateEsIndex()
    search_key = search
    query = qry.create_complex_query(search_key)

    t = es.search(index="review_pos", body=query)
    doc_list = t.body['hits']['hits']
    hit_docs = [d['_source'] for d in doc_list]
    return {"result": hit_docs}

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)