import pandas as pd
import numpy as np

def engineer_features(raw_crypto_data):
    """
    Expects a DataFrame with recent 'Close', 'Open', 'High', 'Low', 'Volume'.
    Returns the exact 14 features required by the model.
    """
    df = raw_crypto_data.copy()
    
    # Calculate rolling metrics used during your notebook training
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['MA_30'] = df['Close'].rolling(window=30).mean()
    
    df['Close_MA7_Pct'] = (df['Close'] - df['MA_7']) / df['MA_7']
    df['Intraday_Return'] = (df['Close'] - df['Open']) / df['Open']
    
    # Define the 14 feature columns matching your model training
    features = [
        "Daily_Return", "ROC_7", "ROC_30", "Historical_Volatility_7",
        "Historical_Volatility_30", "Norm_Rolling_STD_7", "Close_MA7_Pct",
        "Close_MA30_Pct", "Close_EMA7_Pct", "Close_EMA30_Pct",
        "Norm_Price_Range", "Intraday_Return", "High_Low_Pct", "Volume_Change_Pct"
    ]
    
    # Extract the latest row as a 2D numpy array
    latest_features = df[features].iloc[-1].values.reshape(1, -1)
    
    return latest_features, df['Close'].iloc[-1]