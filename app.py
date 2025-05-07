from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')  # bisa ID pribadi atau grup


def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
        print("Token atau Chat ID belum diset.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, json=payload)

    # Log respons Telegram
    print("Telegram Response:", response.status_code, response.text)


@app.route('/webhook', methods=['POST'])
def webhook():
    if not request.is_json:
        return 'Expected JSON', 400

    data = request.get_json()
    action = data.get('action')
    symbol = data.get('symbol')

    if action and symbol:
        message = f"Sinyal {action.upper()} terdeteksi untuk {symbol}"
        send_telegram_message(message)
        return 'Success', 200

    return 'Bad Request: action or symbol missing', 400


@app.route('/')
def home():
    return 'Bot aktif!', 200


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
