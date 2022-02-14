from requests.auth import HTTPBasicAuth
import requests
import json

f = open('config.json')
config = json.loads(f.read())

url = f"http://{config['host_url']}:9200/product"
res = requests.delete(url, auth=HTTPBasicAuth(config['username'], config['password']))
print(res.text)