import pandas as pd
import joblib
import warnings
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report

# Suppress XGBoost warnings for a clean presentation
warnings.filterwarnings('ignore')

def load_and_prep_data(filepath):
    print("--- Loading and Engineering Features ---")
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Separate features and target
    X = df.drop(columns=['Target_Appreciation'])
    y = df['Target_Appreciation']
    
    # Stationarity: Convert all prices to daily % changes
    # This prevents the model from overfitting to raw price levels
    X = X.pct_change() * 100
    
    # Drop NaNs created by pct_change and rolling windows
    X.dropna(inplace=True)
    y = y.loc[X.index]
    
    print(f"Dataset ready. Training on {len(X)} days with {X.shape[1]} features.")
    return X, y

def train_and_evaluate():
    X, y = load_and_prep_data('inr_macro_dataset.csv')
    
    # IMPORTANT: shuffle=False for time-series data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    print("Tuning XGBoost hyperparameters (This may take a moment)...")
    # Using XGBClassifier for classification
    xgb = XGBClassifier(eval_metric='logloss')
    
    # Grid search for the best model parameters
    param_grid = {
        'max_depth': [3, 5, 7],
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1]
    }
    
    grid = GridSearchCV(xgb, param_grid, cv=3, scoring='accuracy')
    grid.fit(X_train, y_train)
    
    best_model = grid.best_estimator_
    print(f"Best Parameters Found: {grid.best_params_}")
    
    # Save the model
    joblib.dump(best_model, 'inr_predictor_model.pkl')
    print("Model saved as 'inr_predictor_model.pkl'.")
    
    # Evaluate
    preds = best_model.predict(X_test)
    print(f"\nFinal Model Accuracy: {accuracy_score(y_test, preds) * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, preds))
    
    # Display Feature Importances for your presentation
    importances = pd.Series(best_model.feature_importances_, index=X.columns)
    print("\nTop Contributing Features:")
    print(importances.sort_values(ascending=False).head(10))

if __name__ == "__main__":
    train_and_evaluate()