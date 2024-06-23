import requests

url = 'http://127.0.0.1:5000/predict'

data = {
    'user_id': 10
}

response = requests.post(url, data=data).json()

print(response)
