import requests
from app.config import config

"""
Пример тестового запроса (должен что-то возвращать)
"""

url = "http://localhost:5000/api/check-imei"
headers = {
    "Token": f"{config.IMEI_API_TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "imei": "356735111052198",
    "serviceId": 12
}

try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    print(response.text)

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error: {http_err} - {response.text}")

except requests.exceptions.RequestException as req_err:
    print(f"Request error: {req_err}")
