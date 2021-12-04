import requests
import json
from sqlalchemy.exc import ObjectNotExecutableError
import pandas as pd


only_backend = False
port = 3000
if only_backend:
    port = 8000

r = requests.post(f"http://127.0.0.1:{port}/api/fill-dummy-data")
print(r.json())

# with open('json.json', 'r', encoding='utf-8') as f:
#     tmp = json.load(f)

# r = requests.post(f'http://3.17.12.94/api/cameras/{1001}', json=tmp)
# print(r, r.text)

# r = requests.post(f"http://127.0.0.1:{port}/api/add-garbage-info", json={
#     "cameraId": 1,
#     "garbageIndex": 5,
# })
# print(r)

# r = requests.get(f"http://127.0.0.1:{port}/api/cameras/littered-points")
# print(r.json())

# df = pd.read_csv('cameras-data.csv')
# for row in df.iloc:
#     print(row["ID папки"])
#     # break