import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.delete(url) #resource delete karne ki request bhejta hai.

print(response.status_code)