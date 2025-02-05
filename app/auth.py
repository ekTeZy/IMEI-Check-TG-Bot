from flask import request, jsonify, abort
from app.config import config

"""
Проверка токена передаваемого в API запросе
"""

def check_api_key():
    api_key = request.headers.get("Token")
    
    if not api_key:
        abort(401, description="Token is undefined.")
    if api_key != config.IMEI_API_TOKEN:
        abort(403, description="Incorrect token.")

    return api_key  
