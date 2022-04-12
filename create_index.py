from requests.auth import HTTPBasicAuth
import requests
import json

f = open('config.json')
config = json.loads(f.read())

def create_product_index():
    url = f"http://{config['host_url']}:9200/product"

    item = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "analysis": {
                "analyzer": {
                    "analyzer-name": {
                        "type": "custom",
                        "tokenizer": "keyword",
                        "filter": "lowercase"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "prd_id": {
                    "type": "text"
                },
                "title": {
                    "type": "text"
                },
                "url": {
                    "type": "text"
                },
                "brand": {
                    "type": "text"
                },
                "hashtag": {
                    "type": "text"
                },
                "category1": {
                    "type": "text"
                },
                "category2": {
                    "type": "text"
                }
            }
        }
    }
    payload = json.dumps(item)
    headers = {'Content-Type': 'application/json'}
    res = requests.request("PUT", url, headers=headers, data=payload,
                           auth=HTTPBasicAuth(config['username'], config['password']))
    print(res.text)


def create_review_index():
    url = f"http://{config['host_url']}:9200/review"

    item = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            },
            "analysis": {
                "analyzer": {
                    "analyzer-name": {
                        "type": "custom",
                        "tokenizer": "keyword",
                        "filter": "lowercase"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "prd_id": {
                    "type": "text"
                },
                "review_id": {
                    "type": "text"
                },
                "review": {
                    "type": "text"
                },
                "genders": {
                    "type": "rank_features"
                }
            }
        }
    }
    payload = json.dumps(item)
    headers = {'Content-Type': 'application/json'}
    res = requests.request("PUT", url, headers=headers, data=payload,
                           auth=HTTPBasicAuth(config['username'], config['password']))
    print(res.text)


def create_review_nlp_index():
    url = f"http://{config['host_url']}:9200/review_nlp"

    item = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            },
            "analysis": {
                "tokenizer": {
                    "korean_nori_tokenizer": {
                        "type": "nori_tokenizer",
                        "decompound_mode": "mixed"
                    }
                },
                "analyzer": {
                    "nori_analyzer": {
                        "type": "custom",
                        "tokenizer": "korean_nori_tokenizer"
                    }
                },
                "filter": {
                    "nori_posfilter": {"type": "nori_part_of_speech",
                                       "stoptags": ["E", "IC", "J", "MAG", "MM", "NA", "NR", "SC", "SE", "SF", "SH",
                                                    "SL", "SN", "SP", "SSC", "SSO", "SY", "UNA", "UNKNOWN", "VA", "VCN",
                                                    "VCP", "VSV", "VV", "VX", "XPN", "XR", "XSA", "XSN", "XSV"]}
                }
            }
        },
        "mappings": {
            "properties": {
                "prd_id": {
                    "type": "text"
                },
                "review_id": {
                    "type": "text"
                },
                "review": {
                    "type": "text",
                    "fields": {
                        "full": {
                            "type": "keyword"
                        },
                        "nori_mixed": {
                            "type": "text",
                            "analyzer": "nori_analyzer",
                            "search_analyzer": "standard"
                        }
                    }
                },
                "genders": {
                    "type": "rank_features"
                }
            }
        }
    }
    payload = json.dumps(item)
    headers = {'Content-Type': 'application/json'}
    res = requests.request("PUT", url, headers=headers, data=payload,
                           auth=HTTPBasicAuth(config['username'], config['password']))
    print(res.text)


def create_mbti_index():
    url = f"http://{config['host_url']}:9201/mbti"

    item = {
        "settings": {
            "analysis": {
              "analyzer": {
                "nori_mixed": {
                  "tokenizer": "nori_t_mixed",
                  "filter": "shingle"
                },
                "nori_pos_noun": {
                  "type": "custom",
                  "tokenizer": "nori_t_mixed",
                  "filter": "pos_filter"
                }
              },
              "tokenizer": {
                "nori_t_mixed": {
                  "type": "nori_tokenizer",
                  "decompound_mode": "mixed"
                }
              },
              "filter": {
                "pos_filter": {
                  "type": "nori_part_of_speech",
                  "stoptags": [
                    "VV", "VA", "VX", "VCP", "VCN", "MM", "MAG", "MAJ",
                    "IC", "J", "E",
                    "XPN", "XSA", "XSN", "XSV",
                    "SP", "SSC", "SSO", "SC", "SE",
                    "UNA"
                  ]
                }
              }
            }
          },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text"
                },
                "contents": {
                    "type": "text",
                    "fields": {
                        "full": {
                          "type": "keyword"
                        },
                        "nori_mixed": {
                            "type": "text",
                            "analyzer": "nori_mixed",
                            "search_analyzer": "standard"
                        },
                        "nori_noun": {
                          "type": "text",
                          "analyzer": "nori_pos_noun",
                          "search_analyzer": "standard"
                        }
                    }
                },
                "keyword": {
                    "type": "keyword"
                },
                "platform": {
                    "type": "keyword"
                },
                "published_at": {
                    "type": "date"
                },
                "doc_url": {
                  "type": "text"
                },
                "comment_cnt": {
                    "type": "integer"
                },
                "like_cnt": {
                    "type": "integer"
                }
            }
        }
    }
    payload = json.dumps(item)
    headers = {'Content-Type': 'application/json'}
    res = requests.request("PUT", url, headers=headers, data=payload)
    print(res.text)


if __name__ == '__main__':
    create_mbti_index()