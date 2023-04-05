import requests
import json



def signUpRequest(username,password,email):
    s = requests.Session()


    res = s.post('http://localhost:8000/api/player/', data=json.dumps({
    "username": username,
    "email":email,
    "password": password
    }))
    return json.loads(res.text)

def logInRequest(username,password):
    s = requests.Session()

    res = s.post('http://localhost:8000/api/player/login/', data=json.dumps({
    "username": username,
    "password": password
    }))

  
    
    return json.loads(res.text),s
def matchmaking(s):
    res = s.post('http://localhost:8000/api/game/', data=json.dumps({
    "join_code": "",
    "generate_join_code": False
    }))

    print(json.loads(res.text))
    return json.loads(res.text)

def update_board(s,id,move):
    res = s.patch('http://localhost:8000/api/game/',data=json.dumps({
        "id": id,
        "action": "MOVE",
        "move": move
        }))

    print(json.loads(res.text))
    return json.loads(res.text)