import requests

url = "http://127.0.0.1:5000/auth/register"
data = {
    "username": "teste",
    "password": "123456",
    "email": "teste@example.com"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
