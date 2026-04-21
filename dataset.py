import yfinance as yf
import pandas as pd
import datetime

def build_dataset():
    print("--- Starting Pipeline: Fetching Data ---")
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=12 * 365) # 12 years of data for training
    
    # Stable tickers
    tickers = {
        'USD_INR': 'INR=X', 
        'Crude_Oil': 'CL=F', 
        'Dollar_Index': 'UUP', 
        'Gold': 'GC=F', 
        'NIFTY_50': '^NSEI',
        'US_Interest_Rate': '^IRX'
    }
    
    # 1. Fetch Data
    raw_data = yf.download(list(tickers.values()), start=start, end=end, auto_adjust=False)['Close']
    raw_data.rename(columns={v: k for k, v in tickers.items()}, inplace=True)
    
    # 2. Force index to datetime
    raw_data.index = pd.to_datetime(raw_data.index)
    
    # 3. Clean Missing Data
    print("Cleaning data...")
    raw_data.ffill(inplace=True)
    raw_data.bfill(inplace=True)
    
    # 4. Feature Engineering: Technical Indicators
    print("Calculating Technical Indicators (MA, RSI, MACD, Bollinger)...")
    df = raw_data.copy()
    
    # Moving Averages
    df['MA_5'] = df['USD_INR'].rolling(window=5).mean()
    df['MA_20'] = df['USD_INR'].rolling(window=20).mean()
    
    # RSI
    delta = df['USD_INR'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['USD_INR'].ewm(span=12, adjust=False).mean()
    exp2 = df['USD_INR'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    
    # Bollinger Bands
    df['BB_mid'] = df['USD_INR'].rolling(window=20).mean()
    df['BB_std'] = df['USD_INR'].rolling(window=20).std()
    
    # 5. Define Target: 1 if USD/INR price goes DOWN tomorrow (INR Appreciates)
    df['Target_Appreciation'] = (df['USD_INR'].shift(-1) < df['USD_INR']).astype(int)
    
    # Final cleanup
    df.dropna(inplace=True)
    
    # 6. Save
    df.to_csv('inr_macro_dataset.csv')
    print(f"--- SUCCESS: Dataset created with {len(df)} rows and {len(df.columns)} columns ---")
    print(f"Columns: {list(df.columns)}")

if __name__ == "__main__":
    build_dataset()