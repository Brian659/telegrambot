from flask import Flask, request # type: ignore
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')  # bisa ID pribadi atau grup

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get('action')
    symbol = data.get('symbol')
    
    if action and symbol:
        message = f"Sinyal {action.upper()} terdeteksi untuk {symbol}"
        send_telegram_message(message)
        return 'Success', 200

    return 'Bad Request', 400

@app.route('/')
def home():
    return 'Bot aktif!', 200
