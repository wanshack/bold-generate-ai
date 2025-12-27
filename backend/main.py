from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from models import StockAnalysisRequest, StockAnalysisResponse
from stock_service import StockDataService
from technical_indicators import TechnicalIndicatorsService
from ml_models import MLPredictionService
from recommendation_engine import RecommendationEngine
from database import get_supabase_client
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stock_service = StockDataService()
technical_service = TechnicalIndicatorsService()
ml_service = MLPredictionService()
recommendation_engine = RecommendationEngine()

@app.get("/")
async def root():
    return {
        "message": "Stock Prediction & Investment API",
        "version": settings.API_VERSION,
        "endpoints": {
            "analyze": "/api/analyze",
            "stock": "/api/stock/{ticker}",
            "predictions": "/api/predictions/{stock_id}",
            "recommendations": "/api/recommendations/{stock_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/analyze")
async def analyze_stock(request: StockAnalysisRequest):
    try:
        ticker = request.ticker.upper()
        prediction_days = request.prediction_days
        model_type = request.model_type

        stock = stock_service.get_or_create_stock(ticker)
        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")

        stock_id = stock["id"]

        stock_info, hist_data = stock_service.fetch_stock_data(ticker, period="2y")
        if hist_data.empty:
            raise HTTPException(status_code=404, detail=f"No data available for {ticker}")

        stock_service.save_stock_prices(stock_id, hist_data)

        prices = stock_service.get_historical_prices(stock_id, days=365)
        if not prices:
            raise HTTPException(status_code=404, detail="No price data available")

        prices_df = pd.DataFrame(prices)

        indicators_df = technical_service.calculate_indicators(prices_df)
        if not indicators_df.empty:
            technical_service.save_indicators(stock_id, indicators_df)

        ml_result = ml_service.predict(prices_df, model_type=model_type, prediction_days=prediction_days)
        if not ml_result:
            raise HTTPException(status_code=500, detail="Prediction failed")

        latest_price = stock_service.get_latest_price(stock_id)
        current_price = float(latest_price["close"])

        latest_indicators = technical_service.get_latest_indicators(stock_id, limit=1)
        if latest_indicators:
            latest_ind = latest_indicators[0]
            latest_ind["close"] = current_price
            technical_analysis = technical_service.analyze_technical_signals(latest_ind)
        else:
            technical_analysis = {"score": 0.5, "signals": [], "sentiment": "neutral"}

        financial_data = stock_service.get_financial_statements(ticker)

        predicted_price = ml_result["predictions"][-1]["price"] if ml_result["predictions"] else current_price

        recommendation_data = recommendation_engine.generate_recommendation(
            stock_id=stock_id,
            current_price=current_price,
            predicted_price=predicted_price,
            prediction_confidence=ml_result["confidence_score"],
            technical_analysis=technical_analysis,
            financial_data=financial_data
        )

        saved_recommendation = recommendation_engine.save_recommendation(recommendation_data)

        supabase = get_supabase_client()
        for pred in ml_result["predictions"][:prediction_days]:
            pred_data = {
                "stock_id": stock_id,
                "target_date": pred["date"],
                "predicted_price": pred["price"],
                "model_type": model_type,
                "confidence_score": ml_result["confidence_score"],
                "prediction_horizon": prediction_days,
                "features_used": {"mae": ml_result["mae"], "rmse": ml_result["rmse"]}
            }
            supabase.table("predictions").insert(pred_data).execute()

        prev_price = float(prices[0]["close"]) if len(prices) > 1 else current_price
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100

        response = {
            "stock": stock,
            "latest_price": current_price,
            "price_change": price_change,
            "price_change_percent": price_change_pct,
            "historical_prices": prices[-90:],
            "technical_indicators": latest_indicators[:30] if latest_indicators else [],
            "predictions": ml_result["predictions"],
            "recommendation": saved_recommendation,
            "financial_summary": financial_data.get("info", {})
        }

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/{ticker}")
async def get_stock(ticker: str):
    stock = stock_service.get_or_create_stock(ticker)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    return stock

@app.get("/api/predictions/{stock_id}")
async def get_predictions(stock_id: str, limit: int = 30):
    supabase = get_supabase_client()
    result = supabase.table("predictions")\
        .select("*")\
        .eq("stock_id", stock_id)\
        .order("prediction_date", desc=True)\
        .limit(limit)\
        .execute()

    return result.data if result.data else []

@app.get("/api/recommendations/{stock_id}")
async def get_recommendations(stock_id: str, limit: int = 10):
    supabase = get_supabase_client()
    result = supabase.table("recommendations")\
        .select("*")\
        .eq("stock_id", stock_id)\
        .order("recommendation_date", desc=True)\
        .limit(limit)\
        .execute()

    return result.data if result.data else []

@app.get("/api/stocks/search")
async def search_stocks(query: str):
    supabase = get_supabase_client()
    result = supabase.table("stocks")\
        .select("*")\
        .ilike("ticker", f"%{query}%")\
        .limit(10)\
        .execute()

    return result.data if result.data else []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
