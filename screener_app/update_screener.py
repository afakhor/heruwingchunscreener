import yfinance as yf
import json
from screener_logic import active_tickers, calculate_indicators

def run_update():
    print("Sedang mendownload data...")
    results = []
    for ticker in active_tickers:
        # Ubah period ke 3mo supaya lebih aman dapat data > 20 hari
        df = yf.download(ticker, period="3mo", progress=False)
        
        if not df.empty:
            df = calculate_indicators(df)
            
            # CEK INI: Pastikan df tidak None sebelum memproses
            if df is not None:
                last = df.iloc[-1]
                results.append({
                    "ticker": ticker.replace('.JK', ''),
                    "close": round(float(last['Close']), 2),
                    "rsi": round(float(last['rsi']), 2)
                })
            else:
                print(f"Data untuk {ticker} kurang dari 20 hari, dilewati.")
    
    with open('data.json', 'w') as f:
        json.dump({"stocks": results}, f)
    print("Data berhasil disimpan ke data.json")

if __name__ == "__main__":
    run_update()
