from requests import request, post
import json
from random import random
from datetime import datetime, timedelta

url = 'http://localhost:8120/envdata2'
headers = {"X-Auth-Token": "tok123", "Content-Type": "application/json"}
# headers = {"X-Auth-Token": "tok123"}

start_time = datetime(2020, 1, 1, 10, 0, 0)
for i in range(20):
    payload = {
        "timestamp": (start_time + timedelta(seconds=i)).isoformat(),
        "battery": 3.1 + random(),
        "temperature": 25 + 2 * random(),
        "humidity": 58.2 + 1.5 * random(),
        "pressure": 1002.3 + 10 * random(),
        "device": "wireless",
        # "X-Auth-Token": "tok123",
    }

    data = {'data': json.dumps(payload)}

    print(f' json: {json.dumps(payload)}')

    # req = post(url=url, headers=headers, data=data)
    req = post(url=url, headers=headers, json=json.dumps(payload))
    status = req.status_code
    print(f' request status: {status}')
    req.close()
