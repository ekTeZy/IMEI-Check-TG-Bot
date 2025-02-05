import requests
from flask import Blueprint, request, jsonify
from app.auth import check_api_key
from app.config import config

api_bp = Blueprint("api_bp", __name__)

"""
Маршрут для обработки API запроса как API клиентов, так и от бота 
"""

@api_bp.route("/check-imei", methods=["POST"])
def check_imei():
    """
    Маршрут для проверки IMEI через imeicheck.net
    """
    api_token = check_api_key()

    data = request.get_json()
    imei = data.get("imei")
    service_id = data.get("serviceId", 12)

    # валидация imei
    if not imei or not isinstance(imei, str) or len(imei) != 15:
        return jsonify({"detail": "IMEI must contain 15 digits."}), 400

    imei_api_url = config.IMEI_API_URL
    
    # заголовки запроса
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept-Language": "en",
        "Content-Type": "application/json"
    }
    
    # тело запроса
    json_request = {
        "deviceId": imei,
        "serviceId": service_id
    }

    # логгирование адреса, заголовка и тела запроса
    print(f"URL: {imei_api_url}")
    print(f"Headers: {headers}")
    print(f"Request body: {json_request}")

    try:
        response = requests.post(imei_api_url, json=json_request, headers=headers)
        print(f"Response body: {response.text}")

        response.raise_for_status()
        return jsonify(response.json()), response.status_code  

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"detail": f"HTTP error: {http_err}"}), response.status_code  
    except requests.exceptions.RequestException as req_err:
        return jsonify({"detail": f"Request error: {req_err}"}), 500