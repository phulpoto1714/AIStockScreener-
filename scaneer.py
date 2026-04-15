import yfinance as yf
import pandas as pd

def get_psx_signals():
    # 25 Selected Stocks from Cement, Auto, Oil & Gas, and Blue Chips
    tickers = [
        # --- OIL & GAS ---
        "OGDC.KA", "PPL.KA", "MARI.KA", "POL.KA", "SNGP.KA",
        # --- CEMENT ---
        "LUCK.KA", "DGKC.KA", "MLCF.KA", "PIOC.KA", "CHCC.KA",
        # --- AUTO ---
        "HCAR.KA", "INDU.KA", "PSMC.KA", "GHNL.KA", "PAEL.KA",
        # --- TECH & FAMOUS ---
        "SYS.KA", "TRG.KA", "HUBC.KA", "ENGRO.KA", "EFERT.KA",
        # --- BANKING & OTHERS ---
        "HBL.KA", "MCB.KA", "UBL.KA", "MEBL.KA", "PSO.KA"
    ]
    
    results = []

    for t in tickers:
        try:
            # 5 minute interval data fetch karna
            data = yf.download(t, period="1d", interval="5m")
            
            # Agar market abhi khuli hai aur kam az kam 3 candles (15 mins) ban chuki hain
            if len(data) >= 3:
                # Pehle 3 candles (0, 1, 2 index) ki high aur low
                opening_range = data.iloc[:3]
                high_15 = opening_range['High'].max()
                low_15 = opening_range['Low'].min()
                
                # Latest Price (Current Price)
                current_price = data['Close'].iloc[-1]
                
                signal = "Waiting..."
                color = "white" # Front-end display ke liye

                # Strategy: 15-Min Range Breakout
                if current_price > high_15:
                    signal = "🚀 BUY BREAKOUT"
                    color = "lightgreen"
                elif current_price < low_15:
                    signal = "📉 SELL BREAKDOWN"
                    color = "tomato"
                
                results.append({
                    "Symbol": t.replace(".KA", ""),
                    "Price": round(current_price, 2),
                    "ORB_High": round(high_15, 2),
                    "ORB_Low": round(low_15, 2),
                    "Signal": signal,
                    "Color": color
                })
        except Exception as e:
            print(f"Error fetching {t}: {e}")
            continue
            
    return results
