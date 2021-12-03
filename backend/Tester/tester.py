import requests
from sqlalchemy.exc import ObjectNotExecutableError

only_backend = False
port = 3000
if only_backend:
    port = 8000

r = requests.post(f"http://127.0.0.1:{port}/api/cameras/fill-dummy-data")
print(r.json())

# r = requests.post(f"http://127.0.0.1:{port}/api/add-garbage-info", json={
#     "cameraId": 1,
#     "garbageIndex": 5,
# })
# print(r)

# r = requests.get(f"http://127.0.0.1:{port}/api/cameras/littered-points")
# print(r.json())