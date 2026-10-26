import requests

try:
    
    response = requests.get( "https://jsonplaceholder.typicode.com/posts/1", timeout=5)

    response.raise_for_status()     #if API response 4xx ya 5xx give error , then rais exception.
    
    print(response.json())

except requests.exceptions.RequestException as e:
    print("API Error:", e)
