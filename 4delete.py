import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.delete(url) #sends request to delete resourse.

print(response.status_code)
