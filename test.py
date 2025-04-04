import requests
import json

url = 'http://127.0.0.1:8000/api/v1/persons/'
headers = {'Content-Type': 'application/json'}
data = {
    "name": "Новый",
    "surname": "Пользователь",
    "username": {
        "username": "newuser1234",
        "password": "securepassword"
    },
    "age": 30,
    "course": [1],
    "role": "2"
}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(f"Код состояния: {response.status_code}")
print(f"Ответ: {response.json()}")