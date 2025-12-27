import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

class MLPredictionService:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def prepare_data(self, prices_df: pd.DataFrame, lookback: int = 60) -> Tuple[np.ndarray, np.ndarray, MinMaxScaler]:
        df = prices_df.copy()
        df = df.sort_values('date')

        data = df[['close']].values
        scaled_data = self.scaler.fit_transform(data)

        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i-lookback:i, 0])
            y.append(scaled_data[i, 0])

        return np.array(X), np.array(y), self.scaler

    def predict_with_xgboost(self, prices_df: pd.DataFrame, prediction_days: int = 30) -> Dict:
        try:
            X, y, scaler = self.prepare_data(prices_df, lookback=60)

            if len(X) < 100:
                raise ValueError("Insufficient data for training")

            split = int(len(X) * 0.8)
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            model = xgb.XGBRegressor(
                objective='reg:squarederror',
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))

            confidence = max(0.5, min(0.95, 1 - (rmse * 2)))

            last_sequence = X[-1].reshape(1, -1)
            predictions = []

            for i in range(prediction_days):
                next_pred = model.predict(last_sequence)[0]
                predictions.append(next_pred)

                last_sequence = np.roll(last_sequence, -1)
                last_sequence[0, -1] = next_pred

            predictions_actual = scaler.inverse_transform(
                np.array(predictions).reshape(-1, 1)
            ).flatten()

            last_date = pd.to_datetime(prices_df['date'].max())
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=prediction_days,
                freq='D'
            )

            return {
                "predictions": [
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "price": float(price)
                    }
                    for date, price in zip(future_dates, predictions_actual)
                ],
                "confidence_score": float(confidence),
                "mae": float(mae),
                "rmse": float(rmse),
                "model_type": "xgboost"
            }

        except Exception as e:
            print(f"XGBoost prediction error: {str(e)}")
            return None

    def predict_with_lstm(self, prices_df: pd.DataFrame, prediction_days: int = 30) -> Dict:
        if not TENSORFLOW_AVAILABLE:
            return None

        try:
            X, y, scaler = self.prepare_data(prices_df, lookback=60)

            if len(X) < 100:
                raise ValueError("Insufficient data for training")

            X = X.reshape((X.shape[0], X.shape[1], 1))

            split = int(len(X) * 0.8)
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            model = Sequential([
                LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
                Dropout(0.2),
                LSTM(50, return_sequences=False),
                Dropout(0.2),
                Dense(25),
                Dense(1)
            ])

            model.compile(optimizer='adam', loss='mean_squared_error')
            model.fit(
                X_train, y_train,
                batch_size=32,
                epochs=10,
                validation_split=0.1,
                verbose=0
            )

            y_pred = model.predict(X_test, verbose=0)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))

            confidence = max(0.5, min(0.95, 1 - (rmse * 2)))

            last_sequence = X[-1].reshape(1, X.shape[1], 1)
            predictions = []

            for i in range(prediction_days):
                next_pred = model.predict(last_sequence, verbose=0)[0, 0]
                predictions.append(next_pred)

                last_sequence = np.roll(last_sequence, -1, axis=1)
                last_sequence[0, -1, 0] = next_pred

            predictions_actual = scaler.inverse_transform(
                np.array(predictions).reshape(-1, 1)
            ).flatten()

            last_date = pd.to_datetime(prices_df['date'].max())
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=prediction_days,
                freq='D'
            )

            return {
                "predictions": [
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "price": float(price)
                    }
                    for date, price in zip(future_dates, predictions_actual)
                ],
                "confidence_score": float(confidence),
                "mae": float(mae),
                "rmse": float(rmse),
                "model_type": "lstm"
            }

        except Exception as e:
            print(f"LSTM prediction error: {str(e)}")
            return None

    def predict(self, prices_df: pd.DataFrame, model_type: str = "xgboost", prediction_days: int = 30) -> Dict:
        if model_type == "lstm" and TENSORFLOW_AVAILABLE:
            return self.predict_with_lstm(prices_df, prediction_days)
        else:
            return self.predict_with_xgboost(prices_df, prediction_days)
