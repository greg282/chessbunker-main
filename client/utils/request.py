import requests
import json

# Use requests.Session to keep the login session alive
s = requests.Session()

res = s.post('http://localhost:8000/api/player/login/', data=json.dumps({
    "username": "abcd",
    "password": "abcd"
}))
print(json.loads(res.text))

res2 = s.get('http://localhost:8000/api/player/')
print(res2)
