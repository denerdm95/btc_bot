from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot online"

def run():
    app.run(host='0.0.0.0', port=10000, threaded=True)

def keep_alive():
    t = Thread(target=run)
    t.start()

import requests
import time
import pandas as pd
from ta.momentum import RSIIndicator

# ===== CONFIG =====

TOKEN = "8041013756:AAHMnYZC2LHJ0VT3aRnVXZad5ILAsuQCv8k"
CHAT_ID = "8729665942"

# ==================

ULTIMO_ALERTA = None

def enviar_telegram(msg):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=payload)

keep_alive()

while True:

    try:

        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=4h&limit=200"

        resposta = requests.get(url)

        data = resposta.json()

        closes = [float(candle[4]) for candle in data]

        df = pd.DataFrame(closes, columns=["close"])

        rsi = RSIIndicator(df["close"], window=14).rsi()

        rsi_atual = round(rsi.iloc[-1], 2)

        print(f"RSI atual: {rsi_atual}", flush=True)

        alerta = None

        if rsi_atual <= 30:
            alerta = "30"

        elif rsi_atual <= 40:
            alerta = "40"

        elif rsi_atual >= 70:
            alerta = "70"

        elif rsi_atual >= 60:
            alerta = "60"

        if alerta != ULTIMO_ALERTA and alerta is not None:

            mensagem = f"""
⚠️ ALERTA RSI BTC 4H

RSI cruzou {alerta}

RSI atual: {rsi_atual}
"""

            enviar_telegram(mensagem)

            print("ALERTA ENVIADO")

            ULTIMO_ALERTA = alerta

        time.sleep(300)

    except Exception as erro:

        print("Erro:", erro)

        time.sleep(60)
