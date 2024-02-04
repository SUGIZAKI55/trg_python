import requests

url = 'http://localhost:5000/add_user'
data = {'username': 'user5', 'password_hash': '4444'}

response = requests.post(url, json=data)

print(response.text)
