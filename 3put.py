import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

data = {
    "id": 1,
    "title": "Python",
    "body": "Learning API",
    "userId": 1
}

response = requests.put(url, json=data)
print(response.json())