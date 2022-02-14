import pandas as pd
import numpy as np
import json
import ast

config = json.loads(open('config.json').read())


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