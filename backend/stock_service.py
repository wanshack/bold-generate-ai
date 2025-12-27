import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from database import get_supabase_client
import uuid

class StockDataService:
    def __init__(self):
        self.supabase = get_supabase_client()

    def fetch_stock_data(self, ticker: str, period: str = "1y") -> Tuple[Optional[Dict], pd.DataFrame]:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period=period)

            if hist.empty:
                return None, pd.DataFrame()

            stock_info = {
                "ticker": ticker.upper(),
                "name": info.get("longName", ticker),
                "exchange": info.get("exchange", "UNKNOWN"),
                "sector": info.get("sector", "Unknown"),
                "country": "ID" if ".JK" in ticker.upper() else "US",
                "currency": info.get("currency", "USD")
            }

            return stock_info, hist

        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            return None, pd.DataFrame()

    def get_or_create_stock(self, ticker: str) -> Optional[Dict]:
        ticker = ticker.upper()

        existing = self.supabase.table("stocks").select("*").eq("ticker", ticker).maybeSingle().execute()

        if existing.data:
            return existing.data

        stock_info, hist = self.fetch_stock_data(ticker)
        if not stock_info:
            return None

        result = self.supabase.table("stocks").insert(stock_info).execute()
        return result.data[0] if result.data else None

    def save_stock_prices(self, stock_id: str, hist_data: pd.DataFrame) -> bool:
        try:
            hist_data = hist_data.reset_index()

            for _, row in hist_data.iterrows():
                price_data = {
                    "stock_id": stock_id,
                    "date": row["Date"].strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]),
                    "adjusted_close": float(row["Close"])
                }

                self.supabase.table("stock_prices").upsert(
                    price_data,
                    on_conflict="stock_id,date"
                ).execute()

            return True
        except Exception as e:
            print(f"Error saving stock prices: {str(e)}")
            return False

    def get_historical_prices(self, stock_id: str, days: int = 365) -> list:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        result = self.supabase.table("stock_prices")\
            .select("*")\
            .eq("stock_id", stock_id)\
            .gte("date", start_date)\
            .order("date", desc=False)\
            .execute()

        return result.data if result.data else []

    def get_latest_price(self, stock_id: str) -> Optional[Dict]:
        result = self.supabase.table("stock_prices")\
            .select("*")\
            .eq("stock_id", stock_id)\
            .order("date", desc=True)\
            .limit(1)\
            .maybeSingle()\
            .execute()

        return result.data

    def get_financial_statements(self, ticker: str) -> Dict[str, Any]:
        try:
            stock = yf.Ticker(ticker)

            financial_data = {
                "income_statement": stock.income_stmt.to_dict() if hasattr(stock, 'income_stmt') else {},
                "balance_sheet": stock.balance_sheet.to_dict() if hasattr(stock, 'balance_sheet') else {},
                "cash_flow": stock.cashflow.to_dict() if hasattr(stock, 'cashflow') else {},
                "info": {
                    "marketCap": stock.info.get("marketCap"),
                    "trailingPE": stock.info.get("trailingPE"),
                    "forwardPE": stock.info.get("forwardPE"),
                    "priceToBook": stock.info.get("priceToBook"),
                    "debtToEquity": stock.info.get("debtToEquity"),
                    "returnOnEquity": stock.info.get("returnOnEquity"),
                    "revenueGrowth": stock.info.get("revenueGrowth"),
                    "earningsGrowth": stock.info.get("earningsGrowth")
                }
            }

            return financial_data
        except Exception as e:
            print(f"Error fetching financial statements: {str(e)}")
            return {}
