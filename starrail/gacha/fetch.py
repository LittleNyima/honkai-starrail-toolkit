import json

import requests


def fetch_json(url):
    r = requests.get(url)
    content = r.content.decode('utf-8')
    return json.loads(content)
