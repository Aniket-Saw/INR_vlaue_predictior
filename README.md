# INR Currency Trend Predictor

A machine learning pipeline for predicting INR/USD currency trends using XGBoost classification with technical indicators and macroeconomic features.

## 📋 Project Overview

This project builds a professional ML pipeline that predicts the directional movement of the INR (Indian Rupee) against the USD. It combines:
- **Historical financial data** from multiple sources (crude oil, dollar index, gold prices, NIFTY-50, US interest rates)
- **Technical indicators** (Moving Averages, RSI, MACD, Bollinger Bands)
- **XGBoost classifier** for directional prediction

The application includes a Streamlit web interface for live market predictions and manual scenario testing.

## 📊 Features

- **Multi-Asset Analysis**: Incorporates 6+ macroeconomic indicators
- **Technical Indicators**: MA, RSI, MACD, and Bollinger Bands
- **Stationary Data Processing**: Converts prices to percentage changes to prevent overfitting
- **Live Market Integration**: Fetches real-time data using yfinance
- **Interactive Web UI**: Streamlit-based interface for predictions
- **Model Tuning**: GridSearchCV hyperparameter optimization

## 🏗️ Project Structure

```
├── app.py                      # Streamlit web application
├── dataset.py                  # Data pipeline (fetch, clean, engineer features)
├── xgboost_cprd.py            # Model training and evaluation
├── inr_macro_dataset.csv      # Training dataset
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone or download the project** to your local machine

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencies

- **yfinance** - Fetch financial market data
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning utilities and metrics
- **xgboost** - Gradient boosting classifier
- **streamlit** - Web application framework
- **joblib** - Model serialization

## 🚀 Usage

### 1. Build the Dataset

Generate the training dataset by fetching 12 years of historical data:

```bash
python dataset.py
```

This will:
- Download historical price data for INR, crude oil, dollar index, gold, NIFTY-50, and US interest rates
- Calculate technical indicators
- Create the `inr_macro_dataset.csv` file

### 2. Train the XGBoost Model

Train and evaluate the XGBoost classifier:

```bash
python xgboost_cprd.py
```

This will:
- Load and preprocess the dataset
- Perform hyperparameter tuning with GridSearchCV
- Train the final model
- Save the model as `inr_predictor_model.pkl`
- Display accuracy and classification metrics

### 3. Run the Web Application

Start the Streamlit app for interactive predictions:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Features**:
- View model accuracy metrics
- **Live Market Data Mode**: Predict next day's INR trend using current market data
- **Manual Input Mode**: Test predictions with custom values

## 📈 Model Performance

- **Training Accuracy**: ~68% (as configured in app.py)
- **Model Type**: XGBoost Classifier with optimized hyperparameters
- **Validation Strategy**: Time-series split (no shuffle to maintain temporal integrity)

## 🔧 Technical Details

### Data Processing
- **Stationarity**: Converts raw prices to daily percentage changes (prevents overfitting to price levels)
- **Feature Engineering**: Calculates technical indicators with rolling windows
- **Missing Data**: Forward fill and backward fill strategies

### Key Technical Indicators
- **MA_5, MA_20**: 5-day and 20-day moving averages
- **RSI**: Relative Strength Index (14-period)
- **MACD**: Moving Average Convergence Divergence
- **Bollinger Bands**: Mid-band and standard deviation

### Target Variable
- **Target_Appreciation**: Binary classification (currency appreciation/depreciation)

## 📝 Workflow

1. **Data Collection** → Fetch 12 years of market data via yfinance
2. **Feature Engineering** → Calculate technical indicators
3. **Data Preprocessing** → Convert to stationarity, handle missing values
4. **Model Training** → XGBoost with hyperparameter tuning
5. **Evaluation** → Accuracy, precision, recall metrics
6. **Deployment** → Streamlit web interface for predictions

## 💡 Future Enhancements

- Add ARIMA/LSTM models for time-series comparison
- Implement ensemble methods combining multiple models
- Add sentiment analysis from financial news
- Backtesting framework for historical performance
- Model explainability (SHAP values)

## ⚠️ Disclaimer

This project is for educational and research purposes only. Currency market predictions are inherently uncertain. Do not use this model for real investment decisions without thorough validation and professional financial advice.

## 📧 Notes

- Requires internet connection to fetch real-time data
- Model training may take a few minutes due to GridSearchCV optimization
- All timestamps are in UTC timezone

---

**Last Updated**: March 2026
