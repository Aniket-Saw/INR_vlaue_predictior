import streamlit as st
import pandas as pd
import joblib
import yfinance as yf
import datetime
from sklearn.metrics import accuracy_score


def get_major_reason(input_features):
    # Get feature importances from the model
    importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
    # Calculate contribution: (Input Value) * (Feature Importance)
    # This shows which feature had the highest impact based on its value today
    contribution = input_features.iloc[0].abs() * importances
    top_reason = contribution.idxmax()
    return top_reason, importances[top_reason]

# --- CONFIGURATION ---
tickers = {'USD_INR': 'INR=X', 'Crude_Oil': 'CL=F', 'Dollar_Index': 'UUP', 
           'Gold': 'GC=F', 'NIFTY_50': '^NSEI', 'US_Interest_Rate': '^IRX'}

# --- HELPER FUNCTIONS ---
@st.cache_resource
def load_model():
    return joblib.load('inr_predictor_model.pkl')

def calculate_indicators(df):
    """Adds technical indicators to a dataframe with USD_INR column."""
    df['MA_5'] = df['USD_INR'].rolling(window=5).mean()
    df['MA_20'] = df['USD_INR'].rolling(window=20).mean()
    delta = df['USD_INR'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    exp1 = df['USD_INR'].ewm(span=12, adjust=False).mean()
    exp2 = df['USD_INR'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['BB_mid'] = df['USD_INR'].rolling(window=20).mean()
    df['BB_std'] = df['USD_INR'].rolling(window=20).std()
    return df

model = load_model()

# --- UI START ---
st.title("INR Currency Trend Predictor")
st.write("Professional ML Pipeline for Directional Prediction")

# Metrics
acc = 0.6206
st.metric("Model Accuracy (Training)", f"{acc:.1%}")

st.divider()

# --- PREDICTION MODE ---
mode = st.radio("Select Prediction Mode", ["Live Market Data", "Manual Input"])
end = datetime.datetime.now()
start = end - datetime.timedelta(days=90)

if mode == "Live Market Data":
    if st.button("Predict Tomorrow's Trend"):
        with st.spinner('Calculating...'):
            df = yf.download(list(tickers.values()), start=start, end=end, auto_adjust=False)['Close']
            df.rename(columns={v:k for k,v in tickers.items()}, inplace=True)
            df.ffill(inplace=True)
            df = calculate_indicators(df)
            
            features = df.pct_change() * 100
            latest = features.tail(1)[model.feature_names_in_]
            
            # --- PREDICT ---
            prediction = model.predict(latest)
            
            # --- GET REASON (Inside the button block!) ---
            importances = pd.Series(model.feature_importances_, index=model.feature_names_in_)
            contribution = latest.iloc[0].abs() * importances
            reason = contribution.idxmax()
            weight = importances[reason]
            
            # --- DISPLAY ---
            if prediction[0] == 1: 
                st.success(f"Prediction: INR will APPRECIATE.")
            else: 
                st.error(f"Prediction: INR will DEPRECIATE.")
            
            st.info(f"**Major Driving Factor:** {reason} (Importance: {weight:.2%})")
            
            st.write("Data used for prediction:")
            st.dataframe(latest)
           
            

elif mode == "Manual Input":
    with st.form("manual"):
        # Create inputs for all features used by the model
        input_dict = {col: st.number_input(f"{col} (%)", value=0.0) for col in model.feature_names_in_}
        if st.form_submit_button("Predict"):
            input_df = pd.DataFrame([input_dict])
            prediction = model.predict(input_df)
            # ... (after prediction = model.predict(latest_features)) ...
            
            # Get the reason
            reason, weight = get_major_reason(input_df)
            
            if prediction[0] == 1: 
                st.success(f"Prediction: INR will APPRECIATE.")
            else: 
                st.error(f"Prediction: INR will DEPRECIATE.")
            
            st.info(f"**Major Driving Factor:** {reason} (Global Model Weight: {weight:.2%})")
            
            
# --- PERFORMANCE BACKTEST ---
st.divider()
if st.button("Run 30-Day Backtest"):
    df = yf.download(list(tickers.values()), start=start, end=end, auto_adjust=False)['Close']
    df.rename(columns={v:k for k,v in tickers.items()}, inplace=True)
    df.ffill(inplace=True)
    df = calculate_indicators(df)
    df['Actual'] = (df['USD_INR'].shift(-1) < df['USD_INR']).astype(int)
    
    X = (df.drop(columns=['Actual'], errors='ignore').pct_change() * 100)[model.feature_names_in_].dropna()
    y = df['Actual'].loc[X.index]
    
    y_pred = model.predict(X.tail(30))
    y_true = y.tail(30)
    
    st.metric("30-Day Backtest Accuracy", f"{accuracy_score(y_true, y_pred):.1%}")
    st.line_chart(pd.DataFrame({'Actual': y_true.values, 'Predicted': y_pred}, index=y_true.index))