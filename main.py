mport yfinance as yf
import pandas as pd

# PSX Stocks ki list (Aap mazeed tickers add kar sakte hain)
STOCKS = ["HUBC.KA", "ENGRO.KA", "LUCK.KA", "OGDC.KA", "PPL.KA", "SYS.KA", "HBL.KA"]

def get_signals():
    signals = []
    for ticker in STOCKS:
        try:
            # 5 minute ka data fetch karna
            df = yf.download(ticker, period='1d', interval='5m')
            if len(df) < 3: continue 

            # Pehle 15 minute (3 candles) ki High aur Low
            opening_range = df.iloc[:3]
            high_15 = opening_range['High'].max()
            low_15 = opening_range['Low'].min()
            current_price = df['Close'].iloc[-1]

            # Strategy: Breakout Confirmation
            if current_price > high_15:
                status = "🚀 BUY (Breakout)"
                target = current_price * 1.02 # 2% Target
                sl = low_15 # Stop Loss at 15-min Low
            elif current_price < low_15:
                status = "📉 SELL (Breakdown)"
                target = current_price * 0.98
                sl = high_15
            else:
                status = "⏳ Waiting"
                target = sl = 0

            signals.append({
                "Stock": ticker.replace(".KA", ""),
                "Price": round(current_price, 2),
                "Signal": status,
                "Target": round(target, 2),
                "StopLoss": round(sl, 2)
            })
        except:
            continue
    return signals

# Result print karne ke liye (Deployment ke waqt ye web par show hoga)
print(pd.DataFrame(get_signals()))
