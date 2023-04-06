import requests
import json

# Use requests.Session to keep the login session alive
s = requests.Session()

res = s.post('http://localhost:8000/api/player/ranking/', data=json.dumps({
    "limit": 10,
    "skip": 0
}))
print(json.loads(res.text))


