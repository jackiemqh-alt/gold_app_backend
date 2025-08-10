# Version number
__version__ = "1.0.1"

from flask import Flask, jsonify
import requests
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)

# API Key from environment variable (fallback to default if not set)
API_KEY = os.getenv("GOLD_API_KEY", "goldapi-1yqqsme2uy1xx-io")
API_URL = "https://www.goldapi.io/api/XAU/USD"

@app.route('/')
def home():
    # 首页直接返回交易信号
    return get_gold_signal()

@app.route('/gold_signal')
def get_gold_signal():
    try:
        # 请求 GoldAPI 实时数据
        headers = {"x-access-token": API_KEY, "Content-Type": "application/json"}
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 429:
            logging.warning("Rate limit exceeded when fetching GoldAPI data.")
            return jsonify({"error": "Rate limit exceeded"}), 429
        if response.status_code != 200:
            logging.error(f"Failed to fetch data from GoldAPI: {response.status_code}")
            return jsonify({"error": "Failed to fetch data from GoldAPI"}), 500
        data = response.json()

        # 获取现货黄金价格
        price = data.get("price", 0)

        # 简单交易策略
        if price > 3434:
            signal = "🟢 建议建多单"
        elif price < 3100:
            signal = "🔴 建议建空单"
        else:
            signal = "😴 当前不建议操作"

        return jsonify({
            "current_price": price,
            "trading_signal": signal,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        logging.error(f"Error fetching gold price: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/version')
def get_version():
    return jsonify({"version": __version__})

if __name__ == '__main__':
    app.run(debug=True)