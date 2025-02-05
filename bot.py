import logging
from flask import json
import requests
import telebot
from app.config import config

"""
Телеграмм-Бот
"""

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(config.BOT_TOKEN)

"""
Вспомогательные функции обрабатывающие запросы к API от бота и сообщения боте
"""


def check_imei(imei):
    """
    Отправляет IMEI в локальный API и возвращает ответ
    """
    headers = {"Token": config.IMEI_API_TOKEN, "Content-Type": "application/json"}
    data = {"imei": str(imei), "serviceId": 12}  

    print(f"URL: {config.LOCAL_API_URL}")
    print(f"Headers: {headers}")
    print(f"Request body: {data}")

    # получаем ответ и логгируем ошибки
    try:
        response = requests.post(config.LOCAL_API_URL, json=data, headers=headers)
        print(f"API response: {response.status_code} - {response.text}")

        response.raise_for_status()
        return {"status_code": response.status_code, "data": response.json()}
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
        return {"status_code": response.status_code, "error": str(http_err)}
    
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
        return {"status_code": None, "error": str(req_err)}
    
def escape_markdown(text):
    """
    экранирует спецсимволы для MarkdownV2
    """
    import re
    
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)

def format_imei_response(response):
    """
    формирует сообщение на основе json-ответа API imeicheck.net
    """
    properties = response.get("properties", {})

    image_url = properties.get("image", "")

    # формируем сообщение с характеристиками
    text = (
        f"*Device Info:*\n"
        f"*Model:* {escape_markdown(properties.get('deviceName', 'Unknown'))}\n"
        f"*Description:* {escape_markdown(properties.get('modelDesc', 'N/A'))}\n"
        f"*IMEI 1:* `{escape_markdown(properties.get('imei', 'N/A'))}`\n"
        f"*IMEI 2:* `{escape_markdown(properties.get('imei2', 'N/A'))}`\n"
        f"*Serial:* `{escape_markdown(properties.get('serial', 'N/A'))}`\n"
        f"*MEID:* `{escape_markdown(properties.get('meid', 'N/A'))}`\n"
        f"*Purchase Country:* {escape_markdown(properties.get('purchaseCountry', 'Unknown'))}\n"
        f"*SIM Lock:* {'Locked' if properties.get('simLock') else 'Unlocked'}\n"
        f"*Replacement:* {'Yes' if properties.get('replacement') else 'No'}\n"
        f"*Lost Mode:* {'Lost' if properties.get('lostMode') else 'Not Lost'}\n"
        f"*Repair Coverage:* {'Covered' if properties.get('repairCoverage') else 'Not Covered'}\n"
    )

    return image_url, text



"""
Обработчики сообщений, отправляемых в бота 
"""

# обработчик /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    
    print(config.WHITELIST_USERS)
    
    # проверка на нахождение в белом списке
    if user_id not in config.WHITELIST_USERS:
        bot.send_message(user_id, "Access denied. You aren't in the whitelist.")
        return
    
    bot.send_message(message.chat.id, "Hello! Send me your IMEI (15 digits) and I'll check the status.")

# обработчик сообщений с IMEI
@bot.message_handler(func=lambda message: message.text.isdigit() and len(message.text) == 15)
def handle_imei(message):
    user_id = message.chat.id

    imei = message.text
    bot.send_message(user_id, f"Checking IMEI {imei}...")

    response = check_imei(imei)

    status_code = response.get("status_code")

    if status_code == 422:
        bot.send_message(user_id, "Error: The IMEI you provided is invalid. Please check and try again.")
        return

    if "error" in response:
        bot.send_message(user_id, f"Error: {response['error']}")
        return

    # форматирование ответа в MarkdownV2
    image_url, response_text = format_imei_response(response["data"])

    if image_url:
        bot.send_photo(user_id, image_url, caption=response_text, parse_mode="MarkdownV2")
    else:
        bot.send_message(user_id, response_text, parse_mode="MarkdownV2")



# обработчик некорректных сообщений
@bot.message_handler(func=lambda message: not message.text.isdigit() or len(message.text) != 15)
def invalid_imei(message):
    bot.send_message(message.chat.id, "Please send a valid IMEI (15 digits).")



# обработчик неизвестных команд или сообщений
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.send_message(message.chat.id, "Unknown command or message. Please send a valid IMEI (15 digits) or use /start command.")



if __name__ == "__main__":
    bot.polling(none_stop=True)