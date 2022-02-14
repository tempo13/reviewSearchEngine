import json
import hashlib
import requests
from requests.auth import HTTPBasicAuth
import ast
import pandas as pd
import numpy as np
from datetime import datetime

f = open('config.json')
config = json.loads(f.read())


class ProductInfo(object):

    def __init__(self, prd_id, title, url, brand, tag, category1, category2):
        self.prd_id = prd_id
        self.title = title
        self.url = url
        self.brand = brand
        self.hashtag = tag
        self.category1 = category1
        self.category2 = category2


class ReviewInfo(object):

    def __init__(self, prd_id, review_id, review, male_score, female_score):
        self.prd_id = prd_id
        self.review_id = review_id
        self.review = review
        self.gender = {"male": male_score, "female": female_score}


def get_unique_id(prd_id):
    return hashlib.sha1(str(prd_id).encode('utf-8')).hexdigest()


def json_field_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unable to parse json field")


def post_to_es(item_list: [ProductInfo]):
    url = f"http://{config['host_url']}:9200/product/_doc/"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for item in item_list:
        pk = get_unique_id(item.prd_id)
        r = requests.put(url + pk, data=json.dumps(item.__dict__, indent=4, sort_keys=True, default=json_field_handler),
                         headers=headers, auth=HTTPBasicAuth(config['username'], config['password']))
        if r.status_code > 200:
            print(r.json())


def review_to_es(item_list: [ReviewInfo]):
    url = f"http://{config['host_url']}:9200/review/_doc/"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for item in item_list:
        pk = get_unique_id(item.review_id)
        r = requests.put(url + pk, data=json.dumps(item.__dict__, indent=4, sort_keys=True, default=json_field_handler),
                         headers=headers, auth=HTTPBasicAuth(config['username'], config['password']))
        if r.status_code > 200:
            print(r.json())


def review_nlp_to_es(item_list: [ReviewInfo]):
    url = f"http://{config['host_url']}:9200/review_nlp/_doc/"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for item in item_list:
        pk = get_unique_id(item.review_id)
        r = requests.put(url + pk, data=json.dumps(item.__dict__, indent=4, sort_keys=True, default=json_field_handler),
                         headers=headers, auth=HTTPBasicAuth(config['username'], config['password']))
        if r.status_code > 200:
            print(r.json())


def put_index(item_list: [ReviewInfo], idx_name):
    url = f"http://{config['host_url']}:9200/{idx_name}/_doc/"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    for item in item_list:
        pk = get_unique_id(item.review_id)
        r = requests.put(url + pk, data=json.dumps(item.__dict__, indent=4, sort_keys=True, default=json_field_handler),
                         headers=headers, auth=HTTPBasicAuth(config['username'], config['password']))
        if r.status_code > 200:
            print(r.json())


def review_refine():
    df = pd.read_csv('predict_data.csv')
    item_list = [ReviewInfo(**row.to_dict()) for _, row in df.iterrows()]
    review_to_es(item_list)


def review_nlp():
    df = pd.read_csv('predict_data.csv')
    item_list = [ReviewInfo(**row.to_dict()) for _, row in df.iterrows()]
    review_nlp_to_es(item_list)


def review_token():
    df = pd.read_csv('predict_data.csv')
    item_list = [ReviewInfo(**row.to_dict()) for _, row in df.iterrows()]
    put_index(item_list, 'review_pos')


def refine_info():
    df = pd.read_csv('prd_info.csv')
    df['prd_id'] = df.apply(lambda x : x['url'].replace(config['data_host_site'], ''), axis=1)
    df['category1'] = df.apply(
        lambda x: ast.literal_eval(x['categories'])[0] if len(ast.literal_eval(x['categories'])) > 1 else None, axis=1)
    df['category2'] = df.apply(
        lambda x: ast.literal_eval(x['categories'])[1] if len(ast.literal_eval(x['categories'])) > 1 else None, axis=1)
    df['tag'] = df.apply(lambda x: " ".join(ast.literal_eval(x['hashtag'])) if x['hashtag'] is not np.nan else '',
                         axis=1)
    res = df[['title', 'brand', 'url', 'prd_id', 'category1', 'category2', 'tag']]
    return res


if __name__ == '__main__':
    review_token()
