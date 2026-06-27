from flask import Flask, jsonify
import json
import os
import ctypes # 1. Impor ctypes
import yfinance as yf

app = Flask(__name__)

# 2. Load C++ Engine (Pastikan libengine.so ada di folder yang sama)
lib = ctypes.CDLL(os.path.abspath("libengine.so"))
lib.calculate_rsi.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int]
lib.calculate_rsi.restype = ctypes.c_float

# 3. Helper Function untuk panggil C++
def get_rsi_cepat(price_list, period=14):
    # Konversi list ke array float C++
    arr = (ctypes.c_float * len(price_list))(*[float(x) for x in price_list])
    return lib.calculate_rsi(arr, len(price_list), period)

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            data = json.load(f)
            
        # Contoh implementasi:
        # Jika data.json memiliki list 'history_prices' untuk setiap saham,
        # kita bisa hitung RSI-nya langsung di sini.
        for stock in data.get('stocks', []):
            if 'history_prices' in stock:
                stock['rsi'] = get_rsi_cepat(stock['history_prices'])
            else:
                stock['rsi'] = 0 # Default jika data kurang
                
        return jsonify(data)
    return jsonify({"stocks": [], "error": "Data belum ada"}), 404

@app.route('/api/chart/<ticker>')
def get_chart(ticker):
    df = yf.download(f"{ticker}.JK", period="1mo", progress=False)
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
    app.run(host='0.0.0.0', port=5000)