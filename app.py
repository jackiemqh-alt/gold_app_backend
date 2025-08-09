# Version number
__version__ = "1.0.0"

from flask import Flask, jsonify
import requests

app = Flask(__name__)

#  API Key
API_KEY = "goldapi-1yqqsme2uy1xx-io"
API_URL = "https://www.goldapi.io/api/XAU/USD"

@app.route('/gold_signal')
def get_gold_signal():
    try:
        # 请求 GoldAPI 实时数据
        headers = {"x-access-token": API_KEY, "Content-Type": "application/json"}
        response = requests.get(API_URL, headers=headers)
        if response.status_code != 200:
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
            "trading_signal": signal
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/version')
def get_version():
    return jsonify({"version": __version__})

if __name__ == '__main__':
    app.run(debug=True)