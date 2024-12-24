import requests

r = requests.post('http://127.0.0.1:8000/api/v1/persons',
                  data={"name": "John", "surname": "Osmkd", 'age': 21})

#r = requests.get('http://127.0.0.1:8000/api/v1/persons')

print(r.text)

