from typing import Optional
from fastapi import FastAPI
from create_es_query import CreateEsIndex
import uvicorn

import json
import elasticsearch
import pickle

with open("stopwords.pickle", "rb") as f:
    stopwords = pickle.load(f)

app = FastAPI()
# Docker Es 구성으로 인한 Config 변경 2022.04.29
es = elasticsearch.Elasticsearch([f"http://localhost:9201"])


@app.get('/')
def get_root():
    return {"data": "Hello world 🎖"}


@app.get('/top/keywords/{mbti_type}')
def get_top_keywords(mbti_type: str, q:Optional[str]=None):
    es_query = {
        "size": 0,
        "query": {"match": {"keyword": mbti_type}},
        "aggs": {
            "term_cnt": {
                "terms": {
                    "field": "contents.nori_noun",
                    "size": 1000
                }
            }
        }
    }
    res = es.search(index="mbti_term", body=es_query)
    bkt_list = res.body["aggregations"]["term_cnt"]["buckets"]
    refine_bkt_list = [b for b in bkt_list if b['key'] not in stopwords]
    refine_bkt_list = [r for r in refine_bkt_list if not r['key'].isdigit()]
    return {"data": refine_bkt_list}


@app.get('/top/keywords/regex/{mbti_type}')
def get_top_keywords_regex(mbti_type: str, q: Optional[str]=None):
    if mbti_type not in ["I", "E"]:
        raise

    regex_q = f"{mbti_type}.*"
    es_query = {
        "size": 0,
        "query": {"regexp": {"keyword": regex_q}},
        "aggs": {
            "term_cnt": {
                "terms": {
                    "field": "contents.nori_noun",
                    "size": 1000
                }
            }
        }
    }
    res = es.search(index="mbti_term", body=es_query)
    bkt_list = res.body["aggregations"]["term_cnt"]["buckets"]
    refine_bkt_list = [b for b in bkt_list if b['key'] not in stopwords]
    refine_bkt_list = [r for r in refine_bkt_list if not r['key'].isdigit()]
    return {"data": refine_bkt_list}


@app.get('/top/keywords/search/{mbti_type}/{keyword}')
def get_search_keyword(mbti_type: str, keyword: str, q: Optional[str]=None):
    if mbti_type not in ["I", "E"]:
        raise

    regex_q = f"{mbti_type}.*"
    es_query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "contents": keyword
                        }
                    },
                    {
                        "regexp": {
                            "keyword": regex_q
                        }
                    }
                ]
            }
        },
        "aggs": {
            "term_cnt": {
                "terms": {
                    "field": "contents.nori_noun",
                    "size": 1000
                }
            }
        }
    }
    res = es.search(index="mbti_term", body=es_query)
    bkt_list = res.body["aggregations"]["term_cnt"]["buckets"]
    refine_bkt_list = [b for b in bkt_list if b['key'] not in stopwords]
    refine_bkt_list = [r for r in refine_bkt_list if not r['key'].isdigit()]
    return {"data": refine_bkt_list}



if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)