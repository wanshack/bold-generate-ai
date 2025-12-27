import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

    API_TITLE: str = "Stock Prediction & Investment API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = """
    Stock Price Prediction and Investment Recommendation Platform

    Features:
    - Historical stock data fetching (US & IDX markets)
    - Technical indicators (RSI, MACD, Moving Averages)
    - ML-based price predictions (LSTM & XGBoost)
    - Buy/Hold/Sell recommendations
    - Financial statements analysis
    """

    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080"
    ]

settings = Settings()
