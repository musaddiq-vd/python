""" API se response aane ke baad usko check aur read karne ke liye 3 important properties hain. """

import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts/1"
)

print(response.status_code) 
print(response.json())      #JSON response ko Python dictionary mein convert karta 
print(response.text)        #Response body ko text format mein deta hai

