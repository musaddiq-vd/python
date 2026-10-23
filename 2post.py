import requests

#API endpoint.
url = "https://jsonplaceholder.typicode.com/posts"


#jo information bhejni hai.
data = {                        
    "title": "GenAI",
    "body": "Learning API",
    "userId": 1
}

response = requests.post(url, json=data)    #json=data → data ko JSON format mein send karta hai.

print(response.status_code)
print(response.json())                      #API ka response dikhata hai.