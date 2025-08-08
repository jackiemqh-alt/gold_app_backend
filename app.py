from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/gold_signal')
def get_gold_signal():
    # 假数据价格模拟
    fake_price = 1984.72

    # 策略判断
    if fake_price > 1985:
        signal = "🟢 建议建多单"
    elif fake_price < 1975:
        signal = "🔴 建议建空单"
    else:
        signal = "😴 当前不建议操作"

    return jsonify({
        "current_price": fake_price,
        "trading_signal": signal
    })

if __name__ == '__main__':
    app.run(debug=True)
