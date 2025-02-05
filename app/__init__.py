from flask import Flask
from app.routes import api_bp

"""
Инициализация приложения
"""

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app
