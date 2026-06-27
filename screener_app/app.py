from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify({"stocks": [], "error": "Data belum ada"}), 404

import yfinance as yf # Pastikan ini sudah di import di atas

@app.route('/api/chart/<ticker>')
def get_chart(ticker):
    # Ambil data 1 bulan terakhir
    df = yf.download(f"{ticker}.JK", period="1mo", progress=False)
    
    # Format data untuk candlestick
    chart_data = []
    for index, row in df.iterrows():
        chart_data.append({
            "date": index.strftime('%Y-%m-%d'),
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close']),
            "volume": float(row['Volume'])
        })
    return jsonify(chart_data)


if __name__ == '__main__':
    # Jalankan di localhost agar bisa diakses HP
    app.run(host='0.0.0.0', port=5000)
