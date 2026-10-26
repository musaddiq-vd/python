""" 3 important properties to check and read, after getting response from API. """

import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1"
)

print(response.status_code) 
print(response.json())      #converts JSON response to python dict
print(response.text)        #gives Response body in text format

