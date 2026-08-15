import numpy as np
from .model_loader import MLModelLoader
from .preprocessing import engineer_features

def predict_next_day_price(recent_data_df, model_type='lstm'):
    # 1. Prepare data features and get today's closing price
    model_input, todays_close = engineer_features(recent_data_df)
    
    # 2. Select model
    if model_type == 'lstm':
        model = MLModelLoader.get_lstm_model()
        # Uncomment below if your LSTM strictly requires a 3D tensor shape: (samples, time_steps, features)
        # model_input = model_input.reshape(1, 1, model_input.shape[1])
    else:
        model = MLModelLoader.get_rf_model()
        
    # 3. Predict return
    predicted_return = model.predict(model_input)[0]
    if isinstance(predicted_return, (list, np.ndarray)):
        predicted_return = float(predicted_return[0])
        
    # 4. Inverse transform to target currency price
    predicted_price = todays_close * (1 + predicted_return)
    
    return {
        "todays_close": todays_close,
        "predicted_return_pct": round(predicted_return * 100, 2),
        "predicted_price": round(predicted_price, 2)
    }