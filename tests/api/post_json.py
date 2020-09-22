from requests import request, post
import json

url = 'http://localhost:8120/envdata'
headers = {"X-Auth-Token": "tok123", "Content-Type": "application/json"}
# headers = {"X-Auth-Token": "tok123"}
payload = {
    "battery": 3.85,
    "temperature": 25.36,
    "humidity": 58.2,
    "pressure": 1002.3,
    # "device": "wired",
    # "X-Auth-Token": "tok123",
}

data = {'data': json.dumps(payload)}

print(f' json: {json.dumps(payload)}')

req = post(url=url, headers=headers, json=json.dumps(payload))
status = req.status_code
print(f' request status: {status}')
req.close()
