from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from decimal import Decimal

class StockBase(BaseModel):
    ticker: str
    name: str
    exchange: str
    sector: Optional[str] = None
    country: str = "US"
    currency: str = "USD"

class StockCreate(StockBase):
    pass

class Stock(StockBase):
    id: str
    last_updated: datetime
    created_at: datetime

class StockPrice(BaseModel):
    id: str
    stock_id: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None
    created_at: datetime

class TechnicalIndicator(BaseModel):
    id: str
    stock_id: str
    date: date
    rsi_14: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_12: Optional[float] = None
    ema_26: Optional[float] = None
    created_at: datetime

class FinancialStatement(BaseModel):
    id: str
    stock_id: str
    period_end: date
    statement_type: str
    data: Dict[str, Any]
    created_at: datetime

class Prediction(BaseModel):
    id: str
    stock_id: str
    prediction_date: date
    target_date: date
    predicted_price: float
    actual_price: Optional[float] = None
    model_type: str
    confidence_score: float
    prediction_horizon: int
    features_used: Optional[Dict[str, Any]] = None
    created_at: datetime

class PredictionCreate(BaseModel):
    stock_id: str
    target_date: date
    predicted_price: float
    model_type: str
    confidence_score: float
    prediction_horizon: int
    features_used: Optional[Dict[str, Any]] = None

class Recommendation(BaseModel):
    id: str
    stock_id: str
    recommendation_date: date
    action: str
    confidence_score: float
    target_price: Optional[float] = None
    current_price: float
    technical_score: Optional[float] = None
    fundamental_score: Optional[float] = None
    reasoning: str
    risk_level: Optional[str] = None
    time_horizon: Optional[str] = None
    created_at: datetime

class RecommendationCreate(BaseModel):
    stock_id: str
    action: str
    confidence_score: float
    target_price: Optional[float] = None
    current_price: float
    technical_score: Optional[float] = None
    fundamental_score: Optional[float] = None
    reasoning: str
    risk_level: Optional[str] = None
    time_horizon: Optional[str] = None

class StockAnalysisRequest(BaseModel):
    ticker: str
    prediction_days: int = Field(default=30, ge=7, le=30)
    model_type: str = Field(default="xgboost", pattern="^(lstm|xgboost)$")

class StockAnalysisResponse(BaseModel):
    stock: Stock
    latest_price: float
    price_change: float
    price_change_percent: float
    historical_prices: List[StockPrice]
    technical_indicators: List[TechnicalIndicator]
    predictions: List[Prediction]
    recommendation: Recommendation
    financial_summary: Optional[Dict[str, Any]] = None
