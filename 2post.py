import requests

#API endpoint.
url = "https://jsonplaceholder.typicode.com/posts"


#jo information bhejni hai.
data = {                        
    "title": "GenAI",
    "body": "Learning API",
    "userId": 1
}

response = requests.post(url, json=data)    #json=data → sends data in JSON fromate.

print(response.status_code)
print(response.json())                      #shows response of API.
