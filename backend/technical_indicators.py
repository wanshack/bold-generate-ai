import pandas as pd
import numpy as np
from typing import Dict, List
from database import get_supabase_client
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator

class TechnicalIndicatorsService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def calculate_indicators(self, prices_df: pd.DataFrame) -> pd.DataFrame:
        if prices_df.empty or len(prices_df) < 200:
            return pd.DataFrame()

        df = prices_df.copy()
        df = df.sort_values('date')

        close_prices = df['close']

        rsi = RSIIndicator(close=close_prices, window=14)
        df['rsi_14'] = rsi.rsi()

        macd_indicator = MACD(
            close=close_prices,
            window_slow=26,
            window_fast=12,
            window_sign=9
        )
        df['macd'] = macd_indicator.macd()
        df['macd_signal'] = macd_indicator.macd_signal()
        df['macd_histogram'] = macd_indicator.macd_diff()

        df['sma_20'] = SMAIndicator(close=close_prices, window=20).sma_indicator()
        df['sma_50'] = SMAIndicator(close=close_prices, window=50).sma_indicator()
        df['sma_200'] = SMAIndicator(close=close_prices, window=200).sma_indicator()

        df['ema_12'] = EMAIndicator(close=close_prices, window=12).ema_indicator()
        df['ema_26'] = EMAIndicator(close=close_prices, window=26).ema_indicator()

        return df

    def save_indicators(self, stock_id: str, indicators_df: pd.DataFrame) -> bool:
        try:
            for _, row in indicators_df.iterrows():
                indicator_data = {
                    "stock_id": stock_id,
                    "date": row["date"].strftime("%Y-%m-%d") if hasattr(row["date"], 'strftime') else str(row["date"]),
                    "rsi_14": float(row["rsi_14"]) if pd.notna(row.get("rsi_14")) else None,
                    "macd": float(row["macd"]) if pd.notna(row.get("macd")) else None,
                    "macd_signal": float(row["macd_signal"]) if pd.notna(row.get("macd_signal")) else None,
                    "macd_histogram": float(row["macd_histogram"]) if pd.notna(row.get("macd_histogram")) else None,
                    "sma_20": float(row["sma_20"]) if pd.notna(row.get("sma_20")) else None,
                    "sma_50": float(row["sma_50"]) if pd.notna(row.get("sma_50")) else None,
                    "sma_200": float(row["sma_200"]) if pd.notna(row.get("sma_200")) else None,
                    "ema_12": float(row["ema_12"]) if pd.notna(row.get("ema_12")) else None,
                    "ema_26": float(row["ema_26"]) if pd.notna(row.get("ema_26")) else None
                }

                self.supabase.table("technical_indicators").upsert(
                    indicator_data,
                    on_conflict="stock_id,date"
                ).execute()

            return True
        except Exception as e:
            print(f"Error saving indicators: {str(e)}")
            return False

    def get_latest_indicators(self, stock_id: str, limit: int = 30) -> List[Dict]:
        result = self.supabase.table("technical_indicators")\
            .select("*")\
            .eq("stock_id", stock_id)\
            .order("date", desc=True)\
            .limit(limit)\
            .execute()

        return result.data if result.data else []

    def analyze_technical_signals(self, indicators: Dict) -> Dict[str, any]:
        score = 0.5
        signals = []

        if indicators.get("rsi_14"):
            rsi = indicators["rsi_14"]
            if rsi < 30:
                signals.append("RSI indicates oversold conditions (bullish)")
                score += 0.15
            elif rsi > 70:
                signals.append("RSI indicates overbought conditions (bearish)")
                score -= 0.15
            else:
                signals.append(f"RSI is neutral at {rsi:.2f}")

        if indicators.get("macd") and indicators.get("macd_signal"):
            macd = indicators["macd"]
            macd_signal = indicators["macd_signal"]
            if macd > macd_signal:
                signals.append("MACD is above signal line (bullish)")
                score += 0.1
            else:
                signals.append("MACD is below signal line (bearish)")
                score -= 0.1

        if all(k in indicators for k in ["close", "sma_50", "sma_200"]):
            close = indicators["close"]
            sma_50 = indicators["sma_50"]
            sma_200 = indicators["sma_200"]

            if close > sma_50 > sma_200:
                signals.append("Price above both 50-day and 200-day MA (strong bullish)")
                score += 0.15
            elif close < sma_50 < sma_200:
                signals.append("Price below both 50-day and 200-day MA (strong bearish)")
                score -= 0.15
            elif close > sma_50:
                signals.append("Price above 50-day MA (bullish)")
                score += 0.05
            else:
                signals.append("Price below 50-day MA (bearish)")
                score -= 0.05

        score = max(0.0, min(1.0, score))

        return {
            "score": score,
            "signals": signals,
            "sentiment": "bullish" if score > 0.6 else "bearish" if score < 0.4 else "neutral"
        }
