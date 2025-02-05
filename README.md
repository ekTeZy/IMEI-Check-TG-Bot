# Telegram IMEI Bot

## Описание

Этот проект — Telegram-бот для проверки IMEI устройств. 
Бот принимает IMEI, отправляет запрос в API imeicheck.net и возвращает пользователю информацию об устройстве.

## Запуск

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Запуск сервера API
```bash
python main.py
```
### или
```bash 
flask run
```

### 3. Запуск бота
```bash
python bot.py
```
## Конфигурация .env
Перед запуском заполните файл .env:
```bash
BOT_TOKEN=your_telegram_bot_token
IMEI_API_TOKEN=your_imei_api_token
IMEI_API_URL=https://api.imeicheck.net/v1/checks
LOCAL_API_URL=http://localhost:5000/api/check-imei
WHITELIST_USERS="123456789 987654321"
```
## Тестирование API
### Запустите test_request.py, чтобы проверить работу API

## Структура проекта
```bash
telegram-imei-bot/
│── app/
│   ├── __init__.py       # Инициализация Flask
│   ├── auth.py           # Проверка API-токена
│   ├── config.py         # Конфигурация
│   ├── routes.py         # API-маршруты
│── bot.py                # Telegram-бот
│── main.py               # Запуск сервера API
│── requirements.txt      # Зависимости
│── test_request.py       # Тестовый запрос
│── .gitignore            # Файлы, игнорируемые Git
│── .env                  # Переменные окружения (не загружать в Git!)
```
